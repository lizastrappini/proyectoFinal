from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum
from src import db

def obtener_entrenadores(categoria=None):
    query = Usuario.query.filter_by(IdRol=3)

    if categoria:
        try:
            categoria_enum = CategoriaEnum[categoria.upper()]
            query = query.filter_by(IdCategoria=categoria_enum.value)
        except KeyError:
            return []

    return [
        {
            'dni': e.Dni,
            'nombre': e.Nombre,
            'apellido': e.Apellido,
            'categoria': CategoriaEnum(e.IdCategoria).name,
        }
        for e in query.all()
    ]
    
def getUsuarioById(id):
    return Usuario.query.filter_by(Id=id).first()


def agregar_entrenador(form):
    dni = form.get('dni')
    nombre = form.get('nombre')
    apellido = form.get('apellido')
    id_categoria = form.get('categoria')

    nuevo_entrenador = Usuario(
        Dni=dni,
        Nombre=nombre,
        Apellido=apellido,
        IdCategoria=id_categoria,
        IdRol=3  # Entrenador
    )

    db.session.add(nuevo_entrenador)
    db.session.commit()