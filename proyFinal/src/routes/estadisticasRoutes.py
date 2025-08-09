from flask import (
    Blueprint, request, render_template, redirect, url_for,
    flash, send_file, jsonify, send_from_directory, session
)
import os
import openpyxl
import io 

import src.controllers.usuarioController as usuarioController
import src.utils.enums.generalEnum as generalEnum

estadisticas_bp = Blueprint('estadisticas', __name__, url_prefix='/estadisticas')

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

@estadisticas_bp.route('/', methods=['GET'])
def index():
    return render_template('estadisticas/index.html')


# Si lo necesitas, puedes descomentar este bloque para subir Excel
# @estadisticas_bp.route('/subir', methods=['POST'])
# def subir_excel():
#     archivo = request.files.get('archivoExcel')
#     if archivo and archivo.filename.endswith(('.xlsx', '.xls')):
#         destino = os.path.join('src', 'datos', archivo.filename)
#         archivo.save(destino)
#         flash("Archivo cargado correctamente", "success")
#     else:
#         flash("Formato inválido. Debe ser .xlsx o .xls", "danger")
#     return redirect(url_for('estadisticas.mostrar_estadisticas'))

def rellenar_excel():
    # Cargar archivo de Excel
    ruta_archivo = "plantilla_estadisticas.xlsx"
    wb = openpyxl.load_workbook(ruta_archivo)
    ws = wb.active  # Hoja activa

    # Buscar columna JUGADOR
    jugador_col_index = None
    jugador_row_index = None
    for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=50, values_only=True), start=1):
        if row:
            for col_idx, value in enumerate(row, start=1):
                if isinstance(value, str) and value.strip().upper() == "JUGADOR":
                    jugador_col_index = col_idx
                    jugador_row_index = row_idx
                    break
        if jugador_col_index:
            break

    if jugador_col_index is None:
        return "No se encontró la columna 'JUGADOR'", 404

    # Lista de usuarios de ejemplo (esto podrías traerlo de usuarioController)
    usuarios = [
        (101, "Juan Pérez"),
        (102, "María López"),
        (103, "Carlos Gómez"),
        (104, "Ana Torres"),
        (105, "Pedro Ramírez")
    ]

    # Rellenar desde la fila siguiente al encabezado
    start_row = jugador_row_index + 1
    for i, (uid, nombre) in enumerate(usuarios, start=start_row):
        ws.cell(row=i, column=jugador_col_index, value=f"#{uid} - {nombre}")

    # Guardar en memoria y devolver
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="plantilla_estadisticas_rellena.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@estadisticas_bp.route('/descargar_plantilla', methods=['GET'])
def descargar_plantilla():
    rellenar_excel()
    ruta = os.path.join('src', 'datos', 'plantilla_de_estadisticas.xlsx')
    return send_file(ruta, as_attachment=True)

@estadisticas_bp.route('/archivos', methods=['GET'])
def listar_archivos():
    carpeta = os.path.join('src', 'datos')
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.xlsx', '.xls'))]
    return jsonify(archivos)

@estadisticas_bp.route('/descargar/<nombre>', methods=['GET'])
def descargar_archivo(nombre):
    carpeta = os.path.join('src', 'datos')
    return send_from_directory(carpeta, nombre, as_attachment=True)

@estadisticas_bp.route('/data', methods=['GET'])
def estadisticas_data():
    # Carga el Excel con valores calculados
    ruta_excel = os.path.join('src', 'datos', 'plantilla_de_estadisticas.xlsx')
    wb = load_workbook(ruta_excel, data_only=True)
    ws = wb.active

    first_row, last_row = 11, 14  # filas de jugadores

    # 1 Sumar por equipo
    team = {}
    for block, cols in BLOCKS.items():
        acc = {sym: 0 for sym in SYMBOLS[block]}
        for col, sym in zip(cols, SYMBOLS[block]):
            for row in range(first_row, last_row + 1):
                val = ws[f"{col}{row}"].value or 0
                acc[sym] += int(val)
        team[block] = acc

    # 2 Estadísticas individuales
    players = []
    for row in range(first_row, last_row + 1):
        jersey = ws[f'D{row}'].value or 0
        stats = {}
        for block, cols in BLOCKS.items():
            stats_block = {}
            for col, sym in zip(cols, SYMBOLS[block]):
                val = ws[f"{col}{row}"].value or 0
                stats_block[sym] = int(val)
            stats[block] = stats_block
        players.append({'jersey': int(jersey), 'stats': stats})

    return jsonify({'team': team, 'players': players})
