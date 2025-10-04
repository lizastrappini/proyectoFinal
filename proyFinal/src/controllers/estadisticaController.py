from datetime import date
from flask import current_app, render_template, url_for
from flask_mail import Message
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, FederadoEnum, RamaEnum
from src import db
from src.models.evento import Evento
from src.models.estadisticaPorPartido import EstadisticaPorPartido
from src.models.estadisticaUsuarioPartido import EstadisticaUsuarioPartido
from datetime import datetime
from sqlalchemy import func, and_, case

def armarEstadisticas(categoria, rama, division, fechaHasta, idPartido=None, idUsuario=None, contrincante=None, misEstadisticas=False):
    filtros_partidos = []

    # --- Filtros básicos ---
    if categoria:
        filtros_partidos.append(EstadisticaPorPartido.IdCategoria == categoria)
    if rama:
        filtros_partidos.append(EstadisticaPorPartido.IdRama == rama)
    if division:
        filtros_partidos.append(EstadisticaPorPartido.IdDivision == division)
    if idPartido:
        filtros_partidos.append(EstadisticaPorPartido.IdPartido == idPartido)
    if contrincante:   
        filtros_partidos.append(EstadisticaPorPartido.IdContrincante == contrincante)

    # --- Filtrar por fecha (rango o día único) ---
    if fechaHasta:
        fecha_desde = None
        fecha_hasta = None
        if "a" in fechaHasta:
            partes = fechaHasta.split("a")
            fecha_desde = datetime.strptime(partes[0].strip(), "%d-%m-%Y").date()
            fecha_hasta = datetime.strptime(partes[1].strip(), "%d-%m-%Y").date()
        else:
            fecha_hasta = datetime.strptime(fechaHasta.strip(), "%d-%m-%Y").date()
            fecha_desde = fecha_hasta

        filtros_partidos.append(EstadisticaPorPartido.Fecha.between(fecha_desde, fecha_hasta))

    # --- Consulta de resumen de partidos ---
    if misEstadisticas and idUsuario:
        partidos_resumen = db.session.query(
            func.count(EstadisticaPorPartido.Id).label("partidos_jugados"),
            func.count(case((EstadisticaPorPartido.Resultado == 1, 1))).label("partidos_ganados"),
            func.count(case((EstadisticaPorPartido.Resultado == 2, 1))).label("partidos_perdidos")
        ).join(
            EstadisticaUsuarioPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
        ).filter(
            *filtros_partidos,
            EstadisticaUsuarioPartido.IdUsuario == idUsuario
        ).one()
    else:
        partidos_resumen = db.session.query(
            func.count(EstadisticaPorPartido.Id).label("partidos_jugados"),
            func.count(case((EstadisticaPorPartido.Resultado == 1, 1))).label("partidos_ganados"),
            func.count(case((EstadisticaPorPartido.Resultado == 2, 1))).label("partidos_perdidos")
        ).filter(*filtros_partidos).one()

    # --- Filtros para usuario ---
    filtros_usuario = filtros_partidos.copy()
    if misEstadisticas and idUsuario:
        filtros_usuario.append(EstadisticaUsuarioPartido.IdUsuario == idUsuario)

    # --- Consulta de estadísticas por usuario ---
    estadisticas_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.RETOTAL).label("recepciones"),
        func.sum(EstadisticaUsuarioPartido.ROTOTAL).label("rotaciones"),
        func.sum(EstadisticaUsuarioPartido.TRTOTAL).label("transiciones"),
        func.sum(EstadisticaUsuarioPartido.SATOTAL).label("saques"),
        func.sum(EstadisticaUsuarioPartido.BLTOTAL).label("bloqueos")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()

    # --- Partidos por categoría ---
    if misEstadisticas and idUsuario:
        partidos_por_categoria = db.session.query(
            EstadisticaPorPartido.IdCategoria,
            func.count(EstadisticaPorPartido.Id).label("cantidad")
        ).join(
            EstadisticaUsuarioPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
        ).filter(
            *filtros_partidos,
            EstadisticaUsuarioPartido.IdUsuario == idUsuario
        ).group_by(EstadisticaPorPartido.IdCategoria).all()
    else:
        partidos_por_categoria = db.session.query(
            EstadisticaPorPartido.IdCategoria,
            func.count(EstadisticaPorPartido.Id).label("cantidad")
        ).filter(*filtros_partidos).group_by(EstadisticaPorPartido.IdCategoria).all()

    partidos_dict = {p.IdCategoria: p.cantidad for p in partidos_por_categoria}

    categorias = []
    cantidades = []
    for cat in generalEnum.CategoriaEnum:
        if cat.value == 0:  # ignorar el enum con valor 0
            continue
        categorias.append(cat.name)
        cantidades.append(partidos_dict.get(cat.value, 0))

    # --- Bloqueos ---
    bloqueos_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.BLP).label("bl_positivos"),
        func.sum(EstadisticaUsuarioPartido.BLN).label("bl_neutros")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()

    # --- Recepciones ---
    recepciones_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.REE).label("REE"),
        func.sum(EstadisticaUsuarioPartido.REV).label("REV"),
        func.sum(EstadisticaUsuarioPartido.RE1).label("RE1"),
        func.sum(EstadisticaUsuarioPartido.RE2).label("RE2"),
        func.sum(EstadisticaUsuarioPartido.RE3).label("RE3")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()

    # --- Rotaciones ---
    rotaciones_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.ROE).label("ROE"),
        func.sum(EstadisticaUsuarioPartido.ROB).label("ROB"),
        func.sum(EstadisticaUsuarioPartido.RO1).label("RO0"),
        func.sum(EstadisticaUsuarioPartido.RO1).label("RO1"),
        func.sum(EstadisticaUsuarioPartido.RO2).label("RO2"),
        func.sum(EstadisticaUsuarioPartido.RO3).label("RO3"),
        func.sum(EstadisticaUsuarioPartido.RO4).label("RO4"),
        func.sum(EstadisticaUsuarioPartido.ROTOTAL).label("ROTOTAL")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()



    # --- Transiciones ---
    transiciones_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.TRE).label("TRE"),
        func.sum(EstadisticaUsuarioPartido.TRB).label("TRB"),
        func.sum(EstadisticaUsuarioPartido.TR0).label("TR0"),
        func.sum(EstadisticaUsuarioPartido.TR1).label("TR1"),
        func.sum(EstadisticaUsuarioPartido.TR2).label("TR2"),
        func.sum(EstadisticaUsuarioPartido.TR3).label("TR3"),
        func.sum(EstadisticaUsuarioPartido.TR4).label("TR4"),
        func.sum(EstadisticaUsuarioPartido.TRTOTAL).label("TRTOTAL")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()


    # --- Saques ---
    saques_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.SA0).label("SA0"),
        func.sum(EstadisticaUsuarioPartido.SA1).label("SA1"),
        func.sum(EstadisticaUsuarioPartido.SA2).label("SA2"),
        func.sum(EstadisticaUsuarioPartido.SA3).label("SA3"),
        func.sum(EstadisticaUsuarioPartido.SA4).label("SA4"),
        func.sum(EstadisticaUsuarioPartido.SATOTAL).label("SATOTAL")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()


    # --- Resumen final ---
    resumen_dict = {
        "partidos_jugados": int(partidos_resumen.partidos_jugados or 0),
        "partidos_ganados": int(partidos_resumen.partidos_ganados or 0),
        "partidos_perdidos": int(partidos_resumen.partidos_perdidos or 0),
        "recepciones": int(estadisticas_resumen.recepciones or 0),
        "rotaciones": int(estadisticas_resumen.rotaciones or 0),
        "transiciones": int(estadisticas_resumen.transiciones or 0),
        "saques": int(estadisticas_resumen.saques or 0),
        "bloqueos": int(estadisticas_resumen.bloqueos or 0),
        "partidos_por_categoria": cantidades,
        "categorias": categorias,
        "bloqueos_positivos": int(bloqueos_resumen.bl_positivos or 0),
        "bloqueos_neutros": int(bloqueos_resumen.bl_neutros or 0),
        "REE": int(recepciones_resumen.REE or 0),
        "REV": int(recepciones_resumen.REV or 0),
        "RE1": int(recepciones_resumen.RE1 or 0),
        "RE2": int(recepciones_resumen.RE2 or 0),
        "RE3": int(recepciones_resumen.RE3 or 0),
        "ROE": int(rotaciones_resumen.ROE or 0),
        "ROB": int(rotaciones_resumen.ROB or 0),
        "RO0": int(rotaciones_resumen.RO0 or 0),
        "RO1": int(rotaciones_resumen.RO1 or 0),
        "RO2": int(rotaciones_resumen.RO2 or 0),
        "RO3": int(rotaciones_resumen.RO3 or 0),
        "RO4": int(rotaciones_resumen.RO4 or 0),
        "ROTOTAL": int(rotaciones_resumen.ROTOTAL or 0),
        "TRE": int(transiciones_resumen.TRE or 0),
        "TRB": int(transiciones_resumen.TRB or 0),
        "TR0": int(transiciones_resumen.TR0 or 0),
        "TR1": int(transiciones_resumen.TR1 or 0),
        "TR2": int(transiciones_resumen.TR2 or 0),
        "TR3": int(transiciones_resumen.TR3 or 0),
        "TR4": int(transiciones_resumen.TR4 or 0),
        "TRTOTAL": int(transiciones_resumen.TRTOTAL or 0),
        "SA0": int(saques_resumen.SA0 or 0),
        "SA1": int(saques_resumen.SA1 or 0),
        "SA2": int(saques_resumen.SA2 or 0),
        "SA3": int(saques_resumen.SA3 or 0),
        "SA4": int(saques_resumen.SA4 or 0),
        "SATOTAL": int(saques_resumen.SATOTAL or 0)
    }

    return resumen_dict

