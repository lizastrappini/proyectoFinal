from flask import (
    Blueprint, request, render_template, redirect, url_for,
    flash, send_file, jsonify, send_from_directory, session
)
import re
import os
import openpyxl
import io 
import datetime
import src.controllers.usuarioController as usuarioController
import src.controllers.calendarioController as calendarioController
import src.utils.enums.generalEnum as generalEnum
from openpyxl.utils import range_boundaries
from src.models.usuario import Usuario
from src.models.estadisticaPorPartido import EstadisticaPorPartido
from src.models.estadisticaUsuarioPartido import EstadisticaUsuarioPartido

from src import db

estadisticas_bp = Blueprint('estadisticas', __name__, url_prefix='/estadisticas')


@estadisticas_bp.route('/', methods=['GET'])
def index():
    return render_template('estadisticas/index.html')

def rellenar_excel(categoria, rama, division, idPartido, ids_seleccionados=None):
    carpeta_actual = os.path.dirname(__file__)
    ruta_archivo = os.path.abspath(os.path.join(carpeta_actual, "..", "datos", "plantilla_de_estadisticas.xlsx"))
    wb = openpyxl.load_workbook(ruta_archivo)
    ws = wb.active

    partido = calendarioController.getPartidosById(int(idPartido))

    if not partido:
        return jsonify({
                "estado": "error",
                "mensaje": f"Partido no encontrado"
            }), 400

    categoria_texto = generalEnum.CategoriaEnum(int(categoria)).name.replace("_", " ").title()
    rama_texto      = generalEnum.RamaEnum(int(rama)).name.replace("_", " ").title()
    division_texto  = generalEnum.DivisionEnum(int(division)).name.replace("_", " ").title()

    # --- NUEVAS CELDAS ---
    # D3
    ws.cell(row=3, column=4, value=f"Rosario Central - {categoria_texto} - {rama_texto} - {division_texto}")

    # O3
    ws.cell(row=3, column=15, value="Contrincante")  # hardcode por ahora

    # P5
    fecha_str = partido.FechaInicio.strftime("%d-%m-%Y")
    ws.cell(row=5, column=16, value=fecha_str)

    # AE3 -> idPartido (siempre presente)
    ws.cell(row=3, column=31, value=partido.Id)

    # --- RELLENAR USUARIOS ---
    usuarios = usuarioController.getUsuarioByCategoriaYRama(categoria, rama, division, ids_seleccionados)
    start_row = 11
    for i, u in enumerate(usuarios, start=start_row):
        ws.cell(row=i, column=1, value=u["Id"])
        ws.cell(row=i, column=2, value=u["Nombre"])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="plantilla_estadisticas_rellena.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@estadisticas_bp.route('/subir_estadisticas', methods=['POST'])
def subir_estadisticas():
    archivo = request.files.get("archivo")
    fecha_str = request.form.get("fecha")  # dd-mm-YYYY
    idPartido = request.form.get("partido")

    if not archivo or not fecha_str or not idPartido:
        return jsonify({"estado": "error", "mensaje": "Faltan datos"}), 400

    try:
        idPartido = int(idPartido)
    except ValueError:
        return jsonify({"estado": "error", "mensaje": "ID de partido inválido"}), 400

    partido = calendarioController.getPartidosById(idPartido)
    if not partido:
        return jsonify({"estado": "error", "mensaje": "No se encontró el partido seleccionado"}), 400

    try:
        wb = openpyxl.load_workbook(archivo)
    except Exception:
        return jsonify({"estado": "error", "mensaje": "No se pudo abrir el archivo Excel"}), 400

    ws = wb.active

    # ---------- VALIDACION DE PARTIDO ----------
    id_partido_excel_value = ws['AE3'].value
    if id_partido_excel_value is None:
        return jsonify({"estado": "error", "mensaje": "No se puede determinar el ID del partido en la planilla"}), 400

    try:
        id_partido_excel = int(str(id_partido_excel_value).strip())
    except ValueError:
        return jsonify({"estado": "error", "mensaje": f"El id del partido de la planilla ('{id_partido_excel_value}') no es válido"}), 400

    if idPartido != id_partido_excel:
        return jsonify({"estado": "error", "mensaje": f"El partido seleccionado no coincide con el de la planilla"}), 400

    # ---------- RESULTADO ----------
    resultado_str = ws['AE5'].value
    if resultado_str not in ['G', 'P']:
        return jsonify({"estado": "error", "mensaje": "Resultado del partido inválido, debe ser 'G' o 'P'"}), 400

    try:
        idResultado = generalEnum.ResultadoEnum[resultado_str].value
    except KeyError:
        return jsonify({"estado": "error", "mensaje": "Resultado del partido no reconocido"}), 400

    # ---------- FECHA ----------
    try:
        fecha_str = fecha_str.strip()
        fecha = datetime.datetime.strptime(fecha_str, "%d-%m-%Y")
    except Exception:
        return jsonify({"estado": "error", "mensaje": "Formato de fecha inválido, debe ser dd-mm-YYYY"}), 400

    # ---------- CREAR ESTADISTICA ----------
    try:
        estadistica = EstadisticaPorPartido(
            Fecha=fecha,
            IdContrincante=partido.IdContrincante,
            IdCategoria=partido.IdCategoria,
            IdRama=partido.IdRama,
            IdDivision=partido.IdDivision,
            Resultado=idResultado,
            IdPartido=partido.Id
        )
        db.session.add(estadistica)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"estado": "error", "mensaje": f"No se pudo guardar la estadística, intente más tarde"}), 500

    # ---------- LEER JUGADORES ----------
    try:
        fila = 11
        while True:
            celda_id = ws.cell(row=fila, column=1).value  # columna A
            if not celda_id:
                break
            try:
                idUsuario = int(celda_id)
            except ValueError:
                return jsonify({"estado": "error", "mensaje": f"ID de usuario inválido en fila {fila}"}), 400

            usuario = Usuario.query.get(idUsuario)
            if usuario:
                rel = EstadisticaUsuarioPartido(
                    IdEstadisticaPorPartido=estadistica.Id,
                    IdUsuario=idUsuario
                )
                db.session.add(rel)
            fila += 1

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"estado": "error", "mensaje": f"Error al guardar los jugadores: {str(e)}"}), 500

    return jsonify({"estado": "ok", "mensaje": "Estadísticas cargadas correctamente"})


@estadisticas_bp.route('/descargar_plantilla', methods=['GET'])
def descargar_plantilla():
    return rellenar_excel()

@estadisticas_bp.route('/archivos', methods=['GET'])
def listar_archivos():
    carpeta = os.path.join('src', 'datos')
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.xlsx', '.xls'))]
    return jsonify(archivos)


@estadisticas_bp.route('/cargar_estadisticas', methods=['GET'])
def cargar_estadisticas():
    
    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    ramas = [
        {'value': r.value, 'text': r.name}
        for r in generalEnum.RamaEnum
    ]
    division = [
        {'value': d.value, 'text': d.name}
        for d in generalEnum.DivisionEnum
        ]
    return render_template('estadisticas/index.html',categorias=categorias, ramas=ramas, division = division)


@estadisticas_bp.route('/descargar_planilla', methods=['GET'])
def descargar_planilla():
    categoria = request.args.get("categoria")
    usuarios = request.args.get("usuarios")  
    rama = request.args.get("rama")
    division = request.args.get("division")
    partido = request.args.get("partido")

    if usuarios:
        ids_seleccionados = [int(x) for x in usuarios.split(",") if x.strip()]
    else:
        ids_seleccionados = None

    if not categoria or not rama or not division or not partido:
        flash("No se selecciono categoria", "danger")
        categorias = [
        {'value': cat.value, 'text': cat.name}
        for cat in generalEnum.CategoriaEnum
        ]
        ramas = [
        {'value': r.value, 'text': r.name}
        for r in generalEnum.RamaEnum
        ]

        division = [
        {'value': d.value, 'text': d.name}
        for d in generalEnum.DivisionEnum
        ]
        return render_template('estadisticas/index.html',categorias=categorias, ramas=ramas, division = division)
    
    return rellenar_excel(categoria,rama, division, partido, ids_seleccionados) 


@estadisticas_bp.route('/usuarios_por_categoria', methods=['GET'])
def usuarios_por_categoria():
    categoria = request.args.get("categoria")
    rama = request.args.get("rama")
    division = request.args.get("division")
    
    if not categoria or not rama or not division:
        return jsonify({"estado": "error", "mensaje": "No se seleccionó filtros"}), 400

    usuarios = usuarioController.getUsuarioByCategoriaYRama(categoria, rama, division)

    return jsonify({"estado": "ok", "usuarios": usuarios})

@estadisticas_bp.route('/partidos_por_categoria', methods=['GET'])
def partidos_por_categoria():
    categoria = request.args.get("categoria")
    fecha = request.args.get("fecha")
    rama = request.args.get("rama")
    division = request.args.get("division")

    if not categoria or not fecha:
        return jsonify({"estado": "error", "mensaje": "No se seleccionó categoría"}), 400

    partidos = calendarioController.getPartidosByCategoria(fecha,categoria, rama, division)

    return jsonify({"estado": "ok", "partidos": partidos})


@estadisticas_bp.route('/partidos_por_categoriayfecha', methods=['GET'])
def partidos_por_categoriayfecha():
    categoria = request.args.get("categoria")
    fecha = request.args.get("fecha")

    if not categoria or not fecha:
        return jsonify({"estado": "error", "mensaje": "No se seleccionó categoría"}), 400

    partidos = calendarioController.getPartidosByCategoriaYFecha(fecha,categoria)

    return jsonify({"estado": "ok", "partidos": partidos})


