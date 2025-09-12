from flask_login import current_user
from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from src import db
from src.models.evento import Evento
from datetime import datetime
from sqlalchemy import func, or_

def crearEvento(nuevoEvento):
    
    db.session.add(nuevoEvento)
    db.session.commit()
    return nuevoEvento

def eliminarEvento(evento):
    db.session.remove(evento)
    db.session.commit()
    
def editarEvento(evento):
     db.session.commit()

def obtenerEventos(inicio,fin,tipos,mi_categoria=None):

    if tipos == []:
        return []
    
    filtros = [
        Evento.FechaInicio <= fin,
        Evento.FechaFin >= inicio
    ]

    if tipos:
        filtros.append(Evento.IdTipoEvento.in_(tipos))

    if mi_categoria == "1" or mi_categoria is True:
        filtros.append(
            or_(
                Evento.IdCategoria == current_user.IdCategoria,
                Evento.IdCategoria == None  # incluye los sin categoría
            )
        )

    eventos = Evento.query.filter(*filtros).all()
    eventosTodos = [
        {
            "id": evento.Id,
            "title": evento.Titulo,
            "start": evento.FechaInicio.isoformat(),
            "end": evento.FechaFin.isoformat(),
            "allDay": evento.TodoElDia,
            "extendedProps": {
                "description": evento.Descripcion,
                "calendar": str(evento.IdTipoEvento),
                "categoria": str(evento.IdCategoria),
                "contrincante": str(evento.IdContrincante),
                "localidad": str(evento.IdLocalidad),
                
                

            }
        } for evento in eventos
    ]
    return eventosTodos

def getPartidosByCategoria(inicio, categoria, rama, division):
    try: 
        fecha_dt = datetime.strptime(inicio, "%d-%m-%Y").date() 
    except ValueError: 
        return [] 
    
    eventos = Evento.query.filter( 
        Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value, 
        Evento.IdCategoria == int(categoria), 
        Evento.TieneEstadistica == False, 
        Evento.IdRama == int(rama), 
        Evento.IdDivision == int(division), 
        func.date(Evento.FechaInicio) == fecha_dt ).all() 
    
    eventosTodos = [ 
        { "value": evento.Id, 
         "text": f"{evento.Titulo} - {generalEnum.RamaEnum(evento.IdRama).name}" } 
        for evento in eventos ] 
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

    # Si es rango, usar between
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

def getPartidosByCategoriaYFecha(inicio, categoria):
    try:
        fecha_dt = datetime.strptime(inicio, "%d-%m-%Y").date()
    except ValueError:
        return []

    eventos = Evento.query.filter(
        Evento.IdTipoEvento == generalEnum.TipoEventoEnum.Partido.value,
        Evento.IdCategoria == int(categoria),  
        Evento.TieneEstadistica == False,
        func.date(Evento.FechaInicio) == fecha_dt
    ).all()

    eventosTodos = [
        {
            "value": evento.Id,
            "text": f"{evento.Titulo} - {generalEnum.RamaEnum(evento.IdRama).name}"
        }
        for evento in eventos
    ]
    return eventosTodos


def getEventoById(id):
    
    evento = Evento.query.filter(
        Evento.Id == id
    ).first()

    return evento

