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

def obtenerEventos(inicio,fin,tipos):
    filtros = [
        Evento.FechaInicio <= fin,
        Evento.FechaFin >= inicio
    ]

    if tipos:
        filtros.append(Evento.IdTipoEvento.in_(tipos))

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
                "localidad": evento.Localidad,
                "calendar": [str(evento.IdTipoEvento)],
                "categoria": [str(evento.IdCategoria)]

            }
        } for evento in eventos
    ]
    return eventosTodos

