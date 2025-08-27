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
    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]

    return render_template('calendario/index.html', tipoeventos=tipoeventos, categorias=categorias)

@calendario_bp.route('/nuevoEvento', methods=['POST'])
def nuevo_evento():
    titulo = request.form.get('titulo')
    tipoEvento = request.form.getlist('tipoEvento')
    fechaInicio = request.form.get('fechaInicio')
    fechaFin = request.form.get('fechaFin')
    todoElDia = request.form.get('todoElDia') == 'on'
    localidad = request.form.get('localidad')
    descripcion = request.form.get('descripcion')
    idCategoria = request.form.get('categoria')
    fecha_inicio_dt = datetime.fromisoformat(fechaInicio.replace('Z', '')) if fechaInicio else None
    fecha_fin_dt = datetime.fromisoformat(fechaFin.replace('Z', '')) if fechaFin else None

    IdTipoEvento = int(tipoEvento[0]) if tipoEvento else None
    IdCategoria = int(idCategoria[0]) if idCategoria else None
    
    nuevo_evento = Evento(
        Titulo=titulo,
        IdTipoEvento=IdTipoEvento,
        FechaInicio=fecha_inicio_dt,
        FechaFin=fecha_fin_dt,
        TodoElDia=todoElDia,
        Localidad=localidad,
        Descripcion=descripcion,
        IdCategoria = IdCategoria
    )
    calendarioController.crearEvento(nuevo_evento)
    return redirect(url_for('calendario.index'))


@calendario_bp.route("/eventos")
def eventos():
    start_str = request.args.get('start')  
    end_str = request.args.get('end')
    tipoEventos = request.args.get('tipoEventos[]')

    if tipoEventos:
        tipos_list = [int(t) for t in tipoEventos.split(',')]
    else:
        tipos_list = []

    start = datetime.fromisoformat(start_str.replace('Z', '')) if start_str else None
    end = datetime.fromisoformat(end_str.replace('Z', '')) if end_str else None
    eventos = calendarioController.obtenerEventos(start, end, tipos_list)
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
    evento.Localidad = data.get('localidad', evento.Localidad)
    evento.Descripcion = data.get('descripcion', evento.Descripcion)
    idCategoria = data.get('categoria')
    evento.IdCategoria = int(idCategoria) if idCategoria else evento.IdCategoria

    calendarioController.editarEvento(evento)
    return jsonify({'mensaje': 'Evento actualizado correctamente'})

@calendario_bp.route('/eliminarEvento/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'error': 'Evento no encontrado'}), 404
    
    return jsonify({'mensaje': 'Evento eliminado correctamente'})

