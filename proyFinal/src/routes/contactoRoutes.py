import secrets
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
from src.controllers import deportistaController, pagosController
from src.models.contacto import Contacto
from src.models.usuario import Usuario
from src.models.pago import Pago
from werkzeug.security import generate_password_hash

from src.utils.enums import generalEnum


contacto_bp = Blueprint('contacto', __name__)
# deportista_bp = Blueprint('deportista', __name__)


@contacto_bp.route('/')
def index():
  
    contactos = Contacto.query.all()

    # Convertirlos a un diccionario con clave = título (por ej: 'telefono') y valor = valor
    contacto_dict = {c.Titulo.lower(): c.Valor for c in contactos}

    return render_template('contacto/contacto.html', contacto=contacto_dict)

# @contacto_bp.route('/obtener', methods=['GET'])
# def obtener():
#     pagos = pagosController.obtener_pagos()
#     return jsonify(data=pagos)  


# @contacto_bp.route('/nuevoPago', methods=['POST'])
# def agregar_pago():
#     try:
        
#         fechaPago = request.form.get('fechaPago')
#         fechaVencimiento = request.form.get('fechaVencimiento')
#         importe = request.form.get('importe')
#         estado_nombre = request.form.get('estado')
#         usuario_id = request.form.get('deportista')
        
#         if not usuario_id:
#             raise ValueError("Debe seleccionar un deportista")
        
#         if not estado_nombre or estado_nombre not in generalEnum.EstadoPagoEnum.__members__:
#             raise ValueError("Estado inválido o no seleccionada")

#         estado_id = generalEnum.EstadoPagoEnum[estado_nombre].value
#         nuevo_pago = Pago(
#             FechaPago= fechaPago,
#             FechaVencimiento=fechaVencimiento,
#             Importe=importe,
#             Estado= estado_id,
#             Usuario_id =int(usuario_id)
#         )
#         pagosController.agregarPago(nuevo_pago)
        

#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return jsonify({'success': True, 'message': 'Pago creado exitosamente'}), 200
#         else:
#             flash('Pago creado exitosamente', 'success')
#             return redirect(url_for('pago.index'))
#     except Exception as e:
#         mensaje_error = str(e)
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return jsonify({'success': False, 'message': mensaje_error}), 400
#         else:
#             flash(f'Error al crear pago: {mensaje_error}', 'danger')
#             return redirect(url_for('pago.index'))



# @contacto_bp.route('/editar/<int:id>', methods=['POST'])
# def editar_pago(id):
#     pago = pagosController.obtener_pago_por_id(id)
#     if not pago:
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return jsonify({'success': False, 'message': 'Pago no encontrado'}), 400
#         else:
#             flash('Pago no encontrado', 'danger')
#             return redirect(url_for('pago.index'))

#     fechaPago = request.form.get('fechaPago')
#     fechaVencimiento = request.form.get('fechaVencimiento')
#     importe = request.form.get('importe')
#     estado_nombre = request.form.get('estado')
#     usuario_id = request.form.get('deportista')
    

#     # Actualiza campos
#     pago.FechaPago = fechaPago
#     pago.FechaVencimiento = fechaVencimiento
#     pago.Importe = importe
#     pago.Estado = generalEnum.EstadoPagoEnum[estado_nombre].value
#     pago.Usuario_id = usuario_id
    

#     pagosController.actualizar_pago(pago)
    
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return jsonify({'success': True, 'message': 'Pago actualizado exitosamente'}), 200
#     else:
#         flash('Pago actualizado exitosamente', 'success')
#         return redirect(url_for('pago.index'))



# @contacto_bp.route('/eliminar/<int:id>', methods=['POST'])
# def eliminar_pago(id):
#     pago = pagosController.obtener_pago_por_id(id)
#     if not pago:
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return jsonify({'success': False, 'message': 'Pago no encontrado'}), 200
#         else:
#             flash('Pago no encontrado', 'danger')
#             return redirect(url_for('pago.index'))
    
#     pagosController.borrar_pago(pago)

#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         return jsonify({'success': True, 'message': 'Pago eliminado'})
#     else:
#         flash('Pago eliminado exitosamente', 'success')
#         return redirect(url_for('pago.index'))
    
    


