import datetime
from decimal import Decimal
import secrets
from flask import Blueprint, current_app, redirect, request, render_template,flash, jsonify, url_for
from flask_login import current_user, login_required
import openpyxl
from src.controllers import deportistaController, pagosController
from src.models.usuario import Usuario
from src.models.pago import Pago

from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename



from src.utils.enums import generalEnum


mispago_bp = Blueprint('mipago', __name__)
# deportista_bp = Blueprint('deportista', __name__)


@mispago_bp.route('/')
def index():
    estados = [
    {'value': estado.value, 'text': estado.name}
    for estado in generalEnum.EstadoPagoEnum
    ]
    deportistas = Usuario.query.filter_by(IdRol=2).all()
    lista_deportistas = [
        {'id': d.Id, 'nombre': f'{d.Nombre} {d.Apellido}'}
        for d in deportistas
    ]
    return render_template('pago/mispagos.html', estados=estados, deportistas=lista_deportistas)  

@mispago_bp.route('/obtener', methods=['GET'])
def obtener():
    pagos = pagosController.obtener_pagos()
    return jsonify(data=pagos)


@mispago_bp.route('/filtrar')
def filtrar():
    estado = request.args.get('estado')
    fecha_desde = request.args.get('fechaDesde')
    fecha_hasta = request.args.get('fechaHasta')
    # dni = request.args.get('dni')
    
    if estado and estado.isdigit():
        estado = int(estado)
    
    data = pagosController.obtener_pagos(estado=estado, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
    return jsonify({'data': data})

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mispago_bp.route("/subir_comprobante/<int:id_pago>", methods=["POST"])
@login_required
def subir_comprobante(id_pago):
    # pago = Pago.query.get(pago_id)
    pago = pagosController.obtener_pago_por_id(id_pago)
    if not pago:
        return jsonify({"success": False, "message": "Pago no encontrado"}), 404

    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No se envió ningún archivo"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "message": "Archivo vacío"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(f"comprobante_{pago.Id}_{file.filename}")
        upload_folder = os.path.join(current_app.root_path, 'static','uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        pago.Comprobante = f"uploads/{filename}"
        pago.IdEstado = generalEnum.EstadoPagoEnum.Pendiente.value
        pagosController.actualizar_pago(pago)
        
        return jsonify({"success": True, "message": "Comprobante subido correctamente", "ruta": pago.Comprobante, "estado": generalEnum.EstadoPagoEnum(pago.IdEstado).name, "filename": filename}), 200

    else:
        return jsonify({"success": False, "message": "Formato de archivo no permitido"}), 400
    