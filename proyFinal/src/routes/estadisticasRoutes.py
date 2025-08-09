#from flask import Blueprint, request, render_template,flash
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
import os
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum
from flask import Blueprint, jsonify, send_from_directory
from openpyxl import load_workbook


estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/estadisticas')
def index():
    return render_template('estadisticas/index.html')

@estadisticas_bp.route('/estadisticas')
def mostrar_estadisticas():
    return render_template('estadisticas/mostrar.html')

"""
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

"""


@estadisticas_bp.route('/descargar_plantilla', methods=['GET'])
def descargar_plantilla():
    ruta = os.path.join('src', 'datos', 'plantilla_estadisticas.xlsx')
    return send_file(ruta, as_attachment=True)




estadisticas_bp = Blueprint('estadisticas_bp', __name__, url_prefix='/estadisticas')

@estadisticas_bp.route('/archivos')
def listar_archivos():
    carpeta = 'datos'
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.xlsx')]
    return jsonify(archivos)

@estadisticas_bp.route('/descargar/<nombre>')
def descargar_archivo(nombre):
    carpeta = 'datos'
    return send_from_directory(carpeta, nombre, as_attachment=True)



estadisticas_bp = Blueprint('estadisticas', __name__)

# Columnas Excel para cada bloque
BLOCKS = {
  'Recepción':      ['E','F','G','H','I','J','K'],
  'Ataque Rotación':['M','N','O','P','Q','R','S'],
  'Ataque Trans.':  ['T','U','V','W','X','Y','Z'],
  'Saque':          ['AA','AB','AC','AD','AE'],
  'Bloqueo':        ['AH','AI']
}

# Símbolos que quieres mostrar, en el mismo orden
SYMBOLS = {
  'Recepción':      ['E','V','=','-','!','+','#'],
  'Ataque Rotación':['E','B','=','-','!','+','#'],
  'Ataque Trans.':  ['E','B','=','-','!','+','#'],
  'Saque':          ['=','-','!','+','#'],
  'Bloqueo':        ['P','N']
}

@estadisticas_bp.route('/estadisticas/data')
def estadisticas_data():
    # Carga el Excel (data_only=True para valores calculados)
    wb = load_workbook('datos/plantilla_de_estadisticas.xlsx', data_only=True)
    ws = wb.active

    first_row, last_row = 11, 14  # filas de jugadores

    # 1) Sumar por equipo
    team = {}
    for block, cols in BLOCKS.items():
        acc = {sym: 0 for sym in SYMBOLS[block]}
        for col, sym in zip(cols, SYMBOLS[block]):
            for row in range(first_row, last_row + 1):
                val = ws[f"{col}{row}"].value or 0
                acc[sym] += int(val)
        team[block] = acc

    # 2) Estadísticas individuales
    players = []
    for row in range(first_row, last_row + 1):
        jersey = ws[f'D{row}'].value or 0
        stats = {}
        for block, cols in BLOCKS.items():
            stats[block] = {}
            for col, sym in zip(cols, SYMBOLS[block]):
                val = ws[f"{col}{row}"].value or 0
                stats[block][sym] = int(val)
        players.append({
            'jersey': int(jersey),
            'stats': stats
        })

    return jsonify({'team': team, 'players': players})
