from flask import Blueprint, request, render_template,flash, redirect, url_for, jsonify
import src.controllers.usuarioController as usuarioController
import src.controllers.calendarioController as calendarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum
from datetime import datetime, timedelta, time
from src.models.evento import Evento
from flask_login import current_user

calendario_bp = Blueprint('calendario', __name__)

eventos_en_memoria = [] 

@calendario_bp.route('/calendario', methods=['GET'])
def index():
    tipoeventos = [
    {'value': evento.value, 'text': evento.name}
    for evento in generalEnum.TipoEventoEnum
    ]
    usuario = current_user
    user = usuarioController.getUsuarioById(usuario.Id)

    if user and (user.IdRol == generalEnum.RolEnum.Deportista.value):
        tipoeventos.append({'value': 7, 'text': 'MiCategoria'})

    if user and (user.IdRol == generalEnum.RolEnum.Entrenador.value or user.IdRol == generalEnum.RolEnum.Admin.value):
        categorias = [
        {'value': cat.value, 'text': cat.name}
        for cat in generalEnum.CategoriaEnum
        if cat.value != 0
]
        contrincantes = [
        {'value': contrincante.value, 'text': contrincante.name}
        for contrincante in generalEnum.ContrincantesEnum
        ]

        localidades = [
        {'value': localidad.value, 'text': localidad.name}
        for localidad in generalEnum.LocalidadEnum
        ]

        ramas = [
        {'value': rama.value, 'text': rama.name}
        for rama in generalEnum.RamaEnum
        ]

        divisiones = [
        {'value': division.value, 'text': division.name}
        for division in generalEnum.DivisionEnum
        ]

        dias = [
        {'value': dia.value, 'text': dia.name}
        for dia in generalEnum.DiasEnum
        ]
        return render_template('calendario/index.html', tipoeventos=tipoeventos, categorias=categorias, contrincantes=contrincantes, localidades=localidades, ramas = ramas, divisiones = divisiones, dias = dias)

    return render_template('calendario/index.html', tipoeventos=tipoeventos)

@calendario_bp.route('/nuevoEvento', methods=['POST'])
def nuevo_evento():
    titulo = request.form.get('titulo')
    tipoEvento = request.form.getlist('tipoEvento')
    fechaInicio = request.form.get('fechaInicio')
    fechaFin = request.form.get('fechaFin')
    todoElDia = request.form.get('todoElDia') == 'on'
    descripcion = request.form.get('descripcion')
    idCategoria = request.form.get('categoria')
    contrintante = request.form.get('contrincante')
    localidad = request.form.get('localidad')
    rama = request.form.get('rama')
    division = request.form.get('division')
    fecha_inicio_dt = datetime.fromisoformat(fechaInicio.replace('Z', '')) if fechaInicio else None
    fecha_fin_dt = datetime.fromisoformat(fechaFin.replace('Z', '')) if fechaFin else None

    IdTipoEvento = int(tipoEvento[0]) if tipoEvento else None
    IdCategoria = int(idCategoria[0]) if idCategoria else None
    Contrincante = int(contrintante[0]) if contrintante else None
    Localidad = int(localidad[0]) if localidad else None
    Rama = int(rama[0]) if rama else None
    Division = int(division[0]) if division else None
    
    eventos_requieren_rama_division = [
        generalEnum.TipoEventoEnum.Entrenamiento.value,
        generalEnum.TipoEventoEnum.Partido.value,
        generalEnum.TipoEventoEnum.Torneo.value
    ]

    if IdTipoEvento in eventos_requieren_rama_division and (Rama is None or Division is None):
        flash("⚠️ Debe seleccionar una rama y una división para este tipo de evento.", "danger")
        return redirect(url_for('calendario.index'))
    
    if IdTipoEvento == generalEnum.TipoEventoEnum.Entrenamiento.value:
        evento_existente = Evento.query.filter(
            Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Entrenamiento.value,
            Evento.IdCategoria == IdCategoria,
            Evento.IdRama == Rama,
            Evento.IdDivision == Division,
            Evento.FechaInicio == fecha_inicio_dt  
        ).first()

        if evento_existente:
            flash("⚠️ Ya existe un entrenamiento para esa categoría en la misma fecha y horario.", "danger")
            return redirect(url_for('calendario.index'))
    
    if(IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value):
        titulo = f"Partido {generalEnum.CategoriaEnum(IdCategoria).name} {generalEnum.RamaEnum(Rama).name} {generalEnum.DivisionEnum(Division).name} vs {generalEnum.ContrincantesEnum(Contrincante).name}"
        fecha_fin_dt = fecha_inicio_dt + timedelta(minutes=1)  

    if(IdTipoEvento == generalEnum.TipoEventoEnum.Recaudacion.value or IdTipoEvento == generalEnum.TipoEventoEnum.SuspensionEntrenamiento.value or IdTipoEvento == generalEnum.TipoEventoEnum.Entrenamiento.value):
        fecha_fin_dt = fecha_inicio_dt + timedelta(minutes=1)  

    if(IdTipoEvento == generalEnum.TipoEventoEnum.Entrenamiento.value):
         titulo = f"Entrenamiento {generalEnum.CategoriaEnum(IdCategoria).name} {generalEnum.RamaEnum(Rama).name} {generalEnum.DivisionEnum(Division).name}"

    if(IdTipoEvento == generalEnum.TipoEventoEnum.Vacaciones.value):
        idCategoria = None
        Rama = None
        Division = None
        Contrincante = None
       
    if(IdTipoEvento == generalEnum.TipoEventoEnum.Torneo.value):
        titulo = f"Torneo {generalEnum.CategoriaEnum(IdCategoria).name} {generalEnum.RamaEnum(Rama).name} {generalEnum.DivisionEnum(Division).name}"

    nuevo_evento = Evento(
        Titulo=titulo,
        IdTipoEvento=IdTipoEvento,
        FechaInicio=fecha_inicio_dt,
        FechaFin=fecha_fin_dt,
        TodoElDia=todoElDia,
        IdLocalidad=Localidad,
        Descripcion=descripcion,
        IdCategoria = IdCategoria,
        IdContrincante= Contrincante,
        IdDivision= Division,
        IdRama= Rama
        
    )

    calendarioController.crearEvento(nuevo_evento)
    flash("✅ Evento creado correctamente", "success")
    return redirect(url_for('calendario.index'))


@calendario_bp.route("/eventos")
def eventos():
    start_str = request.args.get('start')  
    end_str = request.args.get('end')
    tipoEventos = request.args.get('tipoEventos[]')

    mi_categoria = False

    if tipoEventos:
        tipos_list = [int(t) for t in tipoEventos.split(',')]
    else:
        tipos_list = []

    if 7 in tipos_list:
        mi_categoria = True
        if len(tipos_list) == 1:
            tipos_list = [e.value for e in generalEnum.TipoEventoEnum]
    else:
        tipos_list = [t for t in tipos_list if t != 7]

    start = datetime.fromisoformat(start_str.replace('Z', '')) if start_str else None
    end = datetime.fromisoformat(end_str.replace('Z', '')) if end_str else None
    eventos = calendarioController.obtenerEventos(start, end, tipos_list, mi_categoria)

    return jsonify(eventos)
    
@calendario_bp.route("/partidosByCategoria")
def partidosByCategoria(fecha, categoria):

    eventos = calendarioController.getPartidosByCategoria(fecha,categoria)

    return jsonify(eventos)

@calendario_bp.route("/evento/<int:evento_id>")
def evento_detalle(evento_id):
    evento = calendarioController.getEventoById(evento_id)

    tipo = evento.IdTipoEvento
    data = {"id": evento.Id, "tipo": tipo}

    if tipo == generalEnum.TipoEventoEnum.Entrenamiento.value:
        data.update({
            "tipoEvento": generalEnum.TipoEventoEnum(tipo).name,
            "titulo": evento.Titulo,
            "fechaInicio": evento.FechaInicio.strftime("%d-%m-%Y %H:%M")
        })

    elif tipo == generalEnum.TipoEventoEnum.Partido.value:
        data.update({
            "tipoEvento": generalEnum.TipoEventoEnum(tipo).name,
            "categoria": generalEnum.CategoriaEnum(evento.IdCategoria).name if evento.IdCategoria else None,
            "fechaInicio": evento.FechaInicio.strftime("%d-%m-%Y %H:%M"),
            "localidad": generalEnum.LocalidadEnum(evento.IdLocalidad).name if evento.IdLocalidad else None,
            "contrincante": generalEnum.ContrincantesEnum(evento.IdContrincante).name if evento.IdContrincante else None,
            "rama": generalEnum.RamaEnum(evento.IdRama).name if evento.IdRama else None,
            "division": generalEnum.DivisionEnum(evento.IdDivision).name if evento.IdDivision else None
        })

    elif tipo == generalEnum.TipoEventoEnum.Vacaciones.value:
        data.update({
            "tipoEvento": generalEnum.TipoEventoEnum(tipo).name,
            "titulo": evento.Titulo,
            "fechaInicio": evento.FechaInicio.strftime("%d-%m-%Y %H:%M"),
            "fechaFin": evento.FechaFin.strftime("%d-%m-%Y %H:%M") if evento.FechaFin else None
        })

    elif tipo in (generalEnum.TipoEventoEnum.Torneo.value, generalEnum.TipoEventoEnum.Recaudacion.value):
        data.update({
            "tipoEvento": generalEnum.TipoEventoEnum(tipo).name,
            "titulo": evento.Titulo,
            "fechaInicio": evento.FechaInicio.strftime("%d-%m-%Y %H:%M"),
            "fechaFin": evento.FechaFin.strftime("%d-%m-%Y %H:%M") if evento.FechaFin else None,
            "categoria": generalEnum.CategoriaEnum(evento.IdCategoria).name if evento.IdCategoria else None,
            "rama": generalEnum.RamaEnum(evento.IdRama).name if evento.IdRama else None,
            "division": generalEnum.DivisionEnum(evento.IdDivision).name if evento.IdDivision else None,
            "localidad" : generalEnum.LocalidadEnum(evento.IdLocalidad).name if evento.IdLocalidad else None,
            "descripcion": evento.Descripcion 
        })

    elif tipo == generalEnum.TipoEventoEnum.SuspensionEntrenamiento.value:
        data.update({
            "tipoEvento": generalEnum.TipoEventoEnum(tipo).name,
            "titulo": evento.Titulo,
            "fechaInicio": evento.FechaInicio.strftime("%d-%m-%Y %H:%M"),
            "categoria": generalEnum.CategoriaEnum(evento.IdCategoria).name if evento.IdCategoria else None,
            "localidad": generalEnum.LocalidadEnum(evento.IdLocalidad).name if evento.IdLocalidad else None,
            "descripcion": evento.Descripcion
        })

    else:
        data.update({
            "tipoEvento": generalEnum.TipoEventoEnum(tipo).name
        })

    data.update({
            "IdCategoria": generalEnum.CategoriaEnum(evento.IdCategoria).value if evento.IdCategoria else None,
            "IdContrincante": generalEnum.ContrincantesEnum(evento.IdContrincante).value if evento.IdContrincante else None,
            "IdLocalidad": generalEnum.LocalidadEnum(evento.IdLocalidad).value if evento.IdLocalidad else None,
            "IdRama": generalEnum.RamaEnum(evento.IdRama).value if evento.IdRama else None,
            "IdDivision": generalEnum.DivisionEnum(evento.IdDivision).value if evento.IdDivision else None,
            "fechaInicioFormat": evento.FechaInicio.isoformat(),
            "fechaFinFormat": evento.FechaFin.isoformat() if evento.FechaFin else None,
        })

    return jsonify(data)


@calendario_bp.route('/nuevoEventoMasivo', methods=['POST'])
def nuevoEventoMasivo():
    fecha_inicio_str = request.form.get('fechaInicio')
    fecha_fin_str = request.form.get('fechaFin')
    hora_inicio_str = request.form.get('horaInicio') 

    id_categoria = request.form.get('categoriaMasivo')
    id_rama = request.form.get('ramaMasivo')
    id_division = request.form.get('divisionMasivo')
    dias_seleccionados = request.form.getlist('diasMasivo')

    if fecha_inicio_str:
        fecha_inicio_dt = datetime.strptime(fecha_inicio_str.strip(), "%Y-%m-%d")
    else:
        fecha_inicio_dt = None

    if fecha_fin_str:
        fecha_fin_dt = datetime.strptime(fecha_fin_str.strip(), "%Y-%m-%d")
    else:
        fecha_fin_dt = None

    if not fecha_inicio_dt or not fecha_fin_dt or not dias_seleccionados or not hora_inicio_str:
        flash("Debes seleccionar rango de fechas, hora de inicio y al menos un día", "danger")
        return redirect(url_for('calendario.index'))

    if fecha_fin_dt < fecha_inicio_dt:
        flash("La fecha de fin debe ser mayor o igual a la fecha de inicio", "danger")
        return redirect(url_for('calendario.index'))
    
    hora, minuto = map(int, hora_inicio_str.split(":"))
    
    dias_int = [int(d) for d in dias_seleccionados]

    IdCategoria = int(id_categoria) if id_categoria else None
    Rama = int(id_rama) if id_rama else None
    Division = int(id_division) if id_division else None

    fecha_actual = fecha_inicio_dt.date()
    eventos_creados = 0

    while fecha_actual <= fecha_fin_dt.date():
        if fecha_actual.weekday() in dias_int: 
            fecha_inicio_evento = datetime.combine(fecha_actual, time(hora, minuto))
            fecha_fin_evento = fecha_inicio_evento + timedelta(hours=1, minutes=30)

            nuevo_evento = Evento(
                Titulo=f"Entrenamiento {generalEnum.CategoriaEnum(IdCategoria).name} "
                       f"{generalEnum.RamaEnum(Rama).name} "
                       f"{generalEnum.DivisionEnum(Division).name}",
                IdTipoEvento=generalEnum.TipoEventoEnum.Entrenamiento.value,
                FechaInicio=fecha_inicio_evento,
                FechaFin=fecha_fin_evento,
                TodoElDia=False,
                IdCategoria=IdCategoria,
                IdDivision=Division,
                IdRama=Rama,
                Descripcion="Evento creado masivamente"
            )
            calendarioController.crearEvento(nuevo_evento)
            eventos_creados += 1

        fecha_actual += timedelta(days=1)

    flash(f"Se crearon {eventos_creados} entrenamientos masivos", "success")
    return redirect(url_for('calendario.index'))

@calendario_bp.route("/updateEvento/<int:evento_id>", methods=["POST"])
def update_evento(evento_id):
    evento = calendarioController.getEventoById(evento_id)
    if not evento:
        flash("Evento no encontrado", "danger")
        return redirect(url_for("calendario.index"))


    nuevo_titulo = request.form.get("titulo")
    fecha_inicio_str = request.form.get("fechaInicio")
    fecha_fin_str = request.form.get("fechaFin")
    descripcion = request.form.get("descripcion")
    id_tipo_evento = int(request.form.get("tipoEvento")) if request.form.get("tipoEvento") else None
    id_categoria = int(request.form.get("categoria")) if request.form.get("categoria") else None
    id_contrincante = int(request.form.get("contrincante")) if request.form.get("contrincante") else None
    id_localidad = int(request.form.get("localidad")) if request.form.get("localidad") else None
    id_rama = int(request.form.get("rama")) if request.form.get("rama") else None
    id_division = int(request.form.get("division")) if request.form.get("division") else None
    todo_el_dia = request.form.get("todoElDia") == "on"

    fecha_inicio_dt = datetime.fromisoformat(fecha_inicio_str) if fecha_inicio_str else None
    fecha_fin_dt = datetime.fromisoformat(fecha_fin_str) if fecha_fin_str else None


    if id_tipo_evento == generalEnum.TipoEventoEnum.Entrenamiento.value:
        conflicto = Evento.query.filter(
            Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Entrenamiento.value,
            Evento.IdCategoria == id_categoria,
            Evento.IdRama == id_rama,
            Evento.IdDivision == id_division,
            Evento.FechaInicio == fecha_inicio_dt,
            Evento.Id != evento_id  # excluye el actual
        ).first()

        if conflicto:
            flash("⚠️ Ya existe un entrenamiento para esa categoría en la misma fecha y horario.", "danger")
            return redirect(url_for("calendario.index"))


    if id_tipo_evento == generalEnum.TipoEventoEnum.Partido.value:
        nuevo_titulo = f"Partido {generalEnum.CategoriaEnum(id_categoria).name} {generalEnum.RamaEnum(id_rama).name} {generalEnum.DivisionEnum(id_division).name} vs {generalEnum.ContrincantesEnum(id_contrincante).name}"
        fecha_fin_dt = fecha_inicio_dt + timedelta(minutes=1)

    elif id_tipo_evento in (
        generalEnum.TipoEventoEnum.Recaudacion.value,
        generalEnum.TipoEventoEnum.SuspensionEntrenamiento.value,
        generalEnum.TipoEventoEnum.Entrenamiento.value,
    ):
        if id_tipo_evento == generalEnum.TipoEventoEnum.Entrenamiento.value:
            nuevo_titulo = f"Entrenamiento {generalEnum.CategoriaEnum(id_categoria).name} {generalEnum.RamaEnum(id_rama).name} {generalEnum.DivisionEnum(id_division).name}"
        fecha_fin_dt = fecha_inicio_dt + timedelta(minutes=1)

    elif id_tipo_evento == generalEnum.TipoEventoEnum.Vacaciones.value:
        nuevo_titulo = nuevo_titulo or "Vacaciones"
        id_categoria = None
        id_rama = None
        id_division = None
        id_contrincante = None

    elif id_tipo_evento == generalEnum.TipoEventoEnum.Torneo.value:
        nuevo_titulo = f"Torneo {generalEnum.CategoriaEnum(id_categoria).name} {generalEnum.RamaEnum(id_rama).name} {generalEnum.DivisionEnum(id_division).name}"


    evento.Titulo = nuevo_titulo
    evento.FechaInicio = fecha_inicio_dt
    evento.FechaFin = fecha_fin_dt
    evento.Descripcion = descripcion
    evento.IdTipoEvento = id_tipo_evento
    evento.IdCategoria = id_categoria
    evento.IdContrincante = id_contrincante
    evento.IdLocalidad = id_localidad
    evento.IdRama = id_rama
    evento.IdDivision = id_division
    evento.TodoElDia = todo_el_dia

    calendarioController.editarEvento(evento)
    flash("✅ Evento actualizado correctamente", "success")
    return redirect(url_for("calendario.index"))


@calendario_bp.route("/eliminarEvento/<int:evento_id>", methods=["POST"])
def eliminarEvento(evento_id):
    evento = Evento.query.get(evento_id)
    calendarioController.eliminarEvento(evento)
    flash("Evento eliminado correctamente", "success")
    return redirect(url_for("calendario.index"))