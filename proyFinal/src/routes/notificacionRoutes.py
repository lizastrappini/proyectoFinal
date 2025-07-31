from operator import or_
import secrets
import string
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
from src.controllers import deportistaController, notificacionController
from src.models.notificacion import Notificacion
from src.models.usuario import Usuario
from werkzeug.security import generate_password_hash

from src.utils.enums import generalEnum

notificacion_bp = Blueprint('notificacion', __name__)

# @notificacion_bp.route('/')
# def index():
#     return render_template('notificacion/index.html')

@notificacion_bp.route('/')
def index():
    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    notif = notificacionController.obtener_notificaciones()
    return render_template('notificacion/index.html', notificaciones= notif, categorias= categorias)


@notificacion_bp.route('/obtener', methods=['GET'])
def obtener():
    
    notif = notificacionController.obtener_notificaciones()
    return jsonify(data=notif)  

@notificacion_bp.route('/nueva_notificacion', methods=['POST'])
def nueva_notificacion():
    try:
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        categoria_nombre = request.form.get('categoria')
        # categoria = request.form.get('categoria')
        # if categoria is not None and categoria != '':
        #     categoria = int(categoria)
        # else:
        #     categoria = None
        
        if not categoria_nombre:
            categoria_id = None
        else:
            try:
                categoria_enum = generalEnum.CategoriaEnum(int(categoria_nombre))
                categoria_id = categoria_enum.value
            except ValueError:
                raise ValueError("Categoría inválida")
        
       
        nueva_notif = Notificacion(
            Titulo = titulo,
            Descripcion= descripcion,
            Categoria=categoria_id
        )
        
        # if categoria:
        #     usuarios_destino = Usuario.query.filter_by(ategoria=categoria).all()
        # else:
        #     usuarios_destino = Usuario.query.all()
            
        # for user in usuarios_destino:
        #     notificacionController.enviar_mail(user.Email, titulo, descripcion)

        notificacionController.agregarNotificacion(nueva_notif)
        # notificacionController.enviar_mail(nueva_notif)

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
    
    
