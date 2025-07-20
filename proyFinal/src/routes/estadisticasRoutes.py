#from flask import Blueprint, request, render_template,flash
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
import os
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/estadisticas')
def index():
    return render_template('estadisticas/index.html')

@estadisticas_bp.route('/estadisticas')
def mostrar_estadisticas():
    return render_template('estadisticas/mostrar.html')

@estadisticas_bp.route('/estadisticas/subir', methods=['POST'])
def subir_excel():
    archivo = request.files.get('archivoExcel')
    if archivo and archivo.filename.endswith(('.xlsx', '.xls')):
        ruta_destino = os.path.join('src', 'datos', archivo.filename)
        archivo.save(ruta_destino)
        flash("Archivo cargado correctamente", "success")
    else:
        flash("Formato de archivo inválido. Debe ser .xlsx o .xls", "danger")

    return redirect(url_for('estadisticas.mostrar_estadisticas'))


@estadisticas_bp.route('/descargar_plantilla', methods=['GET'])
def descargar_plantilla():
    ruta = os.path.join('src', 'datos', 'plantilla_estadisticas.xlsx')
    return send_file(ruta, as_attachment=True)