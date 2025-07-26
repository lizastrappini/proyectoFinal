from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum
from src import db


def obtener_entrenadores(categoria=None, dni=None):
    query = Usuario.query.filter_by(IdRol=3)

    if categoria:
        try:
            # convertir categoría a int para comparar con el valor del enum
            #categoria_enum = CategoriaEnum[categoria]
            categoria_valor = int(categoria)
            query = query.filter_by(Categoria=str(categoria_valor))
        except KeyError:
            return []
    if dni:
        query = query.filter(Usuario.Dni == int(dni))

    entrenadores = []
    for e in query.all():
        try:
            # convertir e.Categoria (que está como string "2", "3", etc.) a int
            cat_enum = CategoriaEnum(int(e.Categoria))
            categoria_nombre = cat_enum.name # ejemplo: 'Sub14'
        except (ValueError, KeyError):
            categoria_nombre = 'Desconocido'
            

        entrenadores.append({
            'dni': e.Dni,
            'nombre': e.Nombre,
            'apellido': e.Apellido,
            'email': e.Email,
            'telefono': e.Telefono,
            'categoria': categoria_nombre
        })

    return entrenadores

def getUsuarioById(id):
    return Usuario.query.filter_by(Id=id).first()


def agregarEntrenador(nuevoEntrenador):
    db.session.add(nuevoEntrenador)
    db.session.commit()
    return nuevoEntrenador

def actualizar_entrenador(entrenador):
    db.session.commit()
    
def obtener_entrenador_por_dni(dni):
    return Usuario.query.filter_by(Dni=dni, IdRol=3).first()


def borrar_entrenador(entrenador):
    db.session.delete(entrenador)
    db.session.commit()
    # return jsonify({'success': True, 'message': 'Entrenador eliminado'})