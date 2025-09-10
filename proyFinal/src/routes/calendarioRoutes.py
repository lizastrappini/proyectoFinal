from flask import Blueprint, request, render_template,flash, redirect, url_for, jsonify
import src.controllers.usuarioController as usuarioController
import src.controllers.calendarioController as calendarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum
from datetime import datetime
from src.models.evento import Evento

calendario_bp = Blueprint('calendario', __name__)

eventos_en_memoria = [] 

@calendario_bp.route('/calendario', methods=['GET'])
def index():
    tipoeventos = [
    {'value': evento.value, 'text': evento.name}
    for evento in generalEnum.TipoEventoEnum
    ]
    
    tipoeventos.append({'value': 7, 'text': 'MiCategoria'})

    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
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

    return render_template('calendario/index.html', tipoeventos=tipoeventos, categorias=categorias, contrincantes=contrincantes, localidades=localidades, ramas = ramas, divisiones = divisiones)

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
    
    if(IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value):
        titulo = f"Partido {generalEnum.CategoriaEnum(IdCategoria).name} {generalEnum.RamaEnum(Rama).name} {generalEnum.DivisionEnum(Division).name} vs {generalEnum.ContrincantesEnum(Contrincante).name}"
        fecha_fin_dt = fecha_inicio_dt

    if(IdTipoEvento == generalEnum.TipoEventoEnum.Recaudacion.value or IdTipoEvento == generalEnum.TipoEventoEnum.SuspensionEntrenamiento.value or IdTipoEvento == generalEnum.TipoEventoEnum.Entrenamiento.value):
        fecha_fin_dt = fecha_inicio_dt

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
        Localidad=Localidad,
        Descripcion=descripcion,
        IdCategoria = IdCategoria,
        IdContrincante= Contrincante,
        IdDivision= Division,
        IdRama= Rama
        
    )

    calendarioController.crearEvento(nuevo_evento)
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
        tipos_list = [t for t in tipos_list if t != 7]
    else:
        mi_categoria = False

    start = datetime.fromisoformat(start_str.replace('Z', '')) if start_str else None
    end = datetime.fromisoformat(end_str.replace('Z', '')) if end_str else None
    eventos = calendarioController.obtenerEventos(start, end, tipos_list, mi_categoria)

    return jsonify(eventos)
    
@calendario_bp.route('/editarEvento/<int:evento_id>', methods=['PUT'])
def editar_evento(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'error': 'Evento no encontrado'}), 404

    data = request.form
    evento.Titulo = data.get('titulo', evento.Titulo)
    tipoEvento = data.get('tipoEvento')
    evento.IdTipoEvento = int(tipoEvento) if tipoEvento else evento.IdTipoEvento
    evento.FechaInicio = datetime.fromisoformat(data.get('fechaInicio').replace('Z','')) if data.get('fechaInicio') else evento.FechaInicio
    evento.FechaFin = datetime.fromisoformat(data.get('fechaFin').replace('Z','')) if data.get('fechaFin') else evento.FechaFin
    evento.TodoElDia = data.get('todoElDia') == 'on'
    evento.Descripcion = data.get('descripcion', evento.Descripcion)
    idCategoria = data.get('categoria')
    evento.IdCategoria = int(idCategoria) if idCategoria else evento.IdCategoria
    contrincante = data.get('contrincante')
    evento.IdContrincante = int(contrincante) if contrincante else evento.IdContrincante
    localidad = data.get('localidad')
    evento.Localidad = int(localidad) if localidad else evento.Localidad
    

    calendarioController.editarEvento(evento)
    return jsonify({'mensaje': 'Evento actualizado correctamente'})

@calendario_bp.route('/eliminarEvento/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'error': 'Evento no encontrado'}), 404
    
    return jsonify({'mensaje': 'Evento eliminado correctamente'})


@calendario_bp.route("/partidosByCategoria")
def partidosByCategoria(fecha, categoria):

    eventos = calendarioController.getPartidosByCategoria(fecha,categoria)

    return jsonify(eventos)