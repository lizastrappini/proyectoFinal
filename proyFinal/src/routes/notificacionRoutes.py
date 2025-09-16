from sqlalchemy import or_
import secrets
import string
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
from src.controllers import deportistaController, notificacionController
from src.models.notificacion import Notificacion
from src.models.usuario import Usuario
from werkzeug.security import generate_password_hash
from flask_login import current_user
from src.utils.enums import generalEnum

notificacion_bp = Blueprint('notificacion', __name__)


@notificacion_bp.route('/')
def index():
    categorias = [
        {'value': cat.value, 'text': cat.name}
        for cat in generalEnum.CategoriaEnum
    ]
    divisiones = [
        {'value': div.value, 'text': div.name}
        for div in generalEnum.DivisionEnum
    ]
    ramas = [
        {'value': rama.value, 'text': rama.name}
        for rama in generalEnum.RamaEnum
    ]
    notif = notificacionController.obtener_notificaciones()
    
    return render_template(
    'notificacion/index.html',
    notificaciones=notif,
    categorias=categorias,
    divisiones=divisiones,
    ramas=ramas)

@notificacion_bp.route('/filtrar', methods=['GET'])
def filtrar():
    buscar = request.args.get('buscar', '').strip()
    categoria = request.args.get('categoria')
    rama = request.args.get('rama')
    division = request.args.get('division')
    
    
    categoria = int(categoria) if categoria and categoria.isdigit() else None
    rama = int(rama) if rama and rama.isdigit() else None
    division = int(division) if division and division.isdigit() else None
    
    data = notificacionController.obtener_notificaciones(buscar=buscar, categoria=categoria, rama=rama, division=division)
    return jsonify({'data': data})



@notificacion_bp.route('/nueva_notificacion', methods=['POST'])
def nueva_notificacion():
    try:
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        categoria_nombre = request.form.get('categoria')
        division_nombre = request.form.get('division')
        rama_nombre = request.form.get('rama')
    
        if not categoria_nombre:
            categoria_id = None
        else:
            try:
                categoria_enum = generalEnum.CategoriaEnum(int(categoria_nombre))
                categoria_id = categoria_enum.value
            except ValueError:
                raise ValueError("Categoría inválida")
        
        if not division_nombre:
            division_id = None
        else:
            try:
                division_enum = generalEnum.DivisionEnum(int(division_nombre))
                division_id = division_enum.value
            except ValueError:
                raise ValueError("División inválida")
            
        if not rama_nombre:
            rama_id = None
        else:
            try:
                rama_enum = generalEnum.RamaEnum(int(rama_nombre))
                rama_id = rama_enum.value
            except ValueError:
                raise ValueError("Rama inválida")
        
       
        nueva_notif = Notificacion(
            Titulo = titulo,
            Descripcion= descripcion,
            IdCategoria=categoria_id,
            IdDivision=division_id,
            IdRama=rama_id
        )
        notificacionController.agregarNotificacion(nueva_notif)    
        
        
        usuarios_query = Usuario.query

        if categoria_id:
            usuarios_query = usuarios_query.filter_by(IdCategoria=categoria_id)
        if division_id:
            usuarios_query = usuarios_query.filter_by(IdDivision=division_id)
        if rama_id:
            usuarios_query = usuarios_query.filter_by(IdRama=rama_id)

        usuarios_destino = usuarios_query.all()

       
        if usuarios_destino:
            for usuario in usuarios_destino:
                notificacionController.enviar_mail(usuario.Email, titulo, descripcion)
        else:
            # Si no hay filtros o no se encontró nadie, se puede decidir
            # enviar a todos (opcional)
            pass

       

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Notificación creada exitosamente'}), 200
        else:
            flash('Notificación creada exitosamente', 'success')
            return redirect(url_for('notificacion.index'))
    except Exception as e:
        mensaje_error = str(e)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': mensaje_error}), 400
        else:
            flash(f'Error al crear notificación: {mensaje_error}', 'danger')
            return redirect(url_for('notificacion.index'))

@notificacion_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_notificacion(id):
    notificacion = notificacionController.obtener_notif_por_id(id)
    if not notificacion:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Notificación no encontrada'}), 200
        else:
            flash('Notificación no encontrada', 'danger')
            return redirect(url_for('deportista.index'))
    
    notificacionController.borrar_notificacion(notificacion)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Notificación eliminada'})
    else:
        flash('Notificación eliminada exitosamente', 'success')
        return redirect(url_for('notificacion.index'))
    

