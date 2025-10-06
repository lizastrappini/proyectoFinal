from flask_login import current_user
from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from src import db
from src.models.evento import Evento
from datetime import datetime
from sqlalchemy import func, or_, and_, between
def crearEvento(nuevoEvento):
    
    db.session.add(nuevoEvento)
    db.session.commit()
    return nuevoEvento

def eliminarEvento(evento):
    db.session.delete(evento)   
    db.session.commit() 
    
def editarEvento(evento):
     db.session.commit()

from sqlalchemy import or_, and_

def obtenerEventos(inicio, fin, tipos, mi_categoria=None):
    if not tipos:
        return []

    filtros = [
        Evento.FechaInicio <= fin,
        Evento.FechaFin >= inicio
    ]

    if tipos:
        filtros.append(Evento.IdTipoEvento.in_(tipos))

    if mi_categoria == "1" or mi_categoria is True:
        categorias_extra = []
        if getattr(current_user, "categoriaExtra", None):
            categorias_extra = [
                int(x.strip()) for x in current_user.categoriaExtra.split(",") if x.strip().isdigit()
            ]

        filtro_categoria = or_(
            Evento.IdCategoria == current_user.IdCategoria,
            Evento.IdCategoria.in_(categorias_extra) if categorias_extra else False
        )

        filtro_final = and_(
            Evento.IdRama == current_user.IdRama,
            Evento.IdDivision == current_user.IdDivision,
            filtro_categoria
        )

        filtros.append(filtro_final)

    eventos = Evento.query.filter(*filtros).all()

    eventosTodos = [
        {
            "id": evento.Id,
            "title": evento.Titulo,
            "start": evento.FechaInicio.isoformat(),
            "end": evento.FechaFin.isoformat() if evento.FechaFin else None,
            "allDay": evento.TodoElDia,
            "extendedProps": {
                "description": evento.Descripcion,
                "calendar": str(evento.IdTipoEvento),
                "categoria": str(evento.IdCategoria) if evento.IdCategoria else None,
                "rama": str(evento.IdRama) if evento.IdRama else None,
                "division": str(evento.IdDivision) if evento.IdDivision else None,
                "contrincante": str(evento.IdContrincante) if evento.IdContrincante else None,
                "localidad": str(evento.IdLocalidad) if evento.IdLocalidad else None,
            }
        } for evento in eventos
    ]

    return eventosTodos

def getPartidosByCategoria(rango_fechas, categoria, rama, division):
    try:
        inicio_str, fin_str = [f.strip() for f in rango_fechas.split("a")]

        fecha_inicio = datetime.strptime(inicio_str, "%d-%m-%Y").date()
        fecha_fin = datetime.strptime(fin_str, "%d-%m-%Y").date()
    except ValueError:
        return []

    eventos = (
        Evento.query.filter(
            Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value,
            Evento.IdCategoria == int(categoria),
            Evento.TieneEstadistica == False,
            Evento.IdRama == int(rama),
            Evento.IdDivision == int(division),
            func.date(Evento.FechaInicio).between(fecha_inicio, fecha_fin)
        ).all()
    )

    eventosTodos = [
        {
            "value": evento.Id,
            "text": f"{evento.Titulo}"
        }
        for evento in eventos
    ]
    return eventosTodos

def getPartidosByCategoriaMostrar(fechas, categoria, rama, division):
    try:
        partes = fechas.split(" a ")
        if len(partes) == 2:
            inicio = datetime.strptime(partes[0], "%d-%m-%Y").date()
            fin = datetime.strptime(partes[1], "%d-%m-%Y").date()
        else:
            inicio = fin = datetime.strptime(fechas, "%d-%m-%Y").date()
    except ValueError:
        return []

    query = Evento.query.filter(
        Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value,
        Evento.IdCategoria == int(categoria),
        Evento.TieneEstadistica == True,
        Evento.IdRama == int(rama),
        Evento.IdDivision == int(division)
    )

    if inicio != fin:
        query = query.filter(func.date(Evento.FechaInicio).between(inicio, fin))
    else:
        query = query.filter(func.date(Evento.FechaInicio) == inicio)

    eventos = query.all()

    return [
        {
            "value": evento.Id,
            "text": f"{evento.Titulo} - {generalEnum.RamaEnum(evento.IdRama).name}"
        }
        for evento in eventos
    ]

def getPartidosByCategoriaYFecha(fecha, categoria):
    try:
        partes = fecha.split(" a ")
        if len(partes) == 2:
            inicio = datetime.strptime(partes[0], "%d-%m-%Y").date()
            fin = datetime.strptime(partes[1], "%d-%m-%Y").date()
        else:
            inicio = fin = datetime.strptime(fecha, "%d-%m-%Y").date()
    except ValueError:
        return []

    eventos = Evento.query.filter(
        Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value,
        Evento.IdCategoria == int(categoria),  
        Evento.TieneEstadistica == False,
        func.date(Evento.FechaInicio).between(inicio, fin)
    ).all()

    eventosTodos = [
        {
            "value": evento.Id,
            "text": f"{evento.Titulo}"
        }
        for evento in eventos
    ]
    return eventosTodos


def getEventoById(id):
    
    evento = Evento.query.filter(
        Evento.Id == id
    ).first()

    return evento

