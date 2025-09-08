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

def armarEstadisticas(categoria, rama, division, fechaHasta, idPartido=None, idUsuario=None, misEstadisticas=False):
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

    # --- Filtrar por fecha (puede ser un rango o un día único) ---
    if fechaHasta:
        fecha_desde = None
        fecha_hasta = None
        # si es un rango tipo "13-07-2025 a 17-07-2025"
        if "a" in fechaHasta:
            partes = fechaHasta.split("a")
            fecha_desde = datetime.strptime(partes[0].strip(), "%d-%m-%Y").date()
            fecha_hasta = datetime.strptime(partes[1].strip(), "%d-%m-%Y").date()
        else:
            # un solo día
            fecha_hasta = datetime.strptime(fechaHasta.strip(), "%d-%m-%Y").date()
            fecha_desde = fecha_hasta

        filtros_partidos.append(EstadisticaPorPartido.Fecha.between(fecha_desde, fecha_hasta))

    # --- Consulta de resumen de partidos ---
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

    partidos_por_categoria = db.session.query(
        EstadisticaPorPartido.IdCategoria,
        func.count(EstadisticaPorPartido.Id).label("cantidad")
    ).filter(*filtros_partidos).group_by(EstadisticaPorPartido.IdCategoria).all()

    partidos_dict = {p.IdCategoria: p.cantidad for p in partidos_por_categoria}

    
    categorias = []
    cantidades = []

    for cat in generalEnum.CategoriaEnum:
        if cat.value == 0:           # ignorar el enum con valor 0
            continue
        categorias.append(cat.name)  
        cantidades.append(partidos_dict.get(cat.value, 0))

    filtros_bloqueos = filtros_partidos.copy()
    if misEstadisticas and idUsuario:
        filtros_bloqueos.append(EstadisticaUsuarioPartido.IdUsuario == idUsuario)

    bloqueos_resumen = db.session.query(
        func.sum(EstadisticaUsuarioPartido.BLP).label("bl_positivos"),
        func.sum(EstadisticaUsuarioPartido.BLN).label("bl_neutros")
    ).join(
        EstadisticaPorPartido, EstadisticaUsuarioPartido.IdEstadisticaPorPartido == EstadisticaPorPartido.Id
    ).filter(
        *filtros_usuario
    ).one()

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
        "RE3": int(recepciones_resumen.RE3 or 0)
    }

    return resumen_dict
