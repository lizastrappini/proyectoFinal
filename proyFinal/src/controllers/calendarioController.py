from flask_login import current_user
from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from src import db
from src.models.evento import Evento


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
    filtros = [
        Evento.FechaInicio <= fin,
        Evento.FechaFin >= inicio
    ]

    if tipos:
        filtros.append(Evento.IdTipoEvento.in_(tipos))
    if mi_categoria == "1":  # checkbox marcado
        filtros.append(Evento.IdCategoria == current_user.IdCategoria)

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
                "calendar": [str(evento.IdTipoEvento)],
                "categoria": [str(evento.IdCategoria)],
                "contrincante": [str(evento.Contrincante)],
                "localidad": [str(evento.Localidad)],
                
                

            }
        } for evento in eventos
    ]
    return eventosTodos

