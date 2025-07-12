from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from src import db
from werkzeug.security import generate_password_hash

def loginUser(email,password):
    usuario = Usuario.query.filter_by(Email=email, Password=password).first() 
    return usuario



def miCuenta(id):
    usuario = Usuario.query.filter_by(Id=id).first()
    if(usuario is not None):
        return {
            'id': usuario.Id,
            'dni': usuario.Dni,
            'nombre': usuario.Nombre,
            'apellido': usuario.Apellido,
            'email': usuario.Email,
            'password': usuario.Password,
            'usuario': usuario.NombreUsuario,
            'categoria': generalEnum.CategoriaEnum(usuario.IdCategoria).name,
            'localidad': generalEnum.LocalidadEnum(usuario.IdLocalidad).name,
            'estado': generalEnum.EstadoEnum(usuario.IdEstado).name,
            'direccion': usuario.Direccion,
            'telefono': usuario.Telefono,
            'rol': generalEnum.RolEnum(usuario.IdRol).name ,
            'idEstado': usuario.IdEstado,
            'idRol': usuario.IdRol,
        }
    

def getUsuarioById(id):
    return Usuario.query.filter_by(Id=id).first()

def update(id, datos):
    usuario = Usuario.query.filter_by(Id=id).first()

    localidad_enum = generalEnum.LocalidadEnum[datos['Localidad']]
    valor_localidad = localidad_enum.value

    if usuario:
        if 'Nombre' in datos:
            usuario.Nombre = datos['Nombre']
        if 'Apellido' in datos:
            usuario.Apellido = datos['Apellido']
        if 'Email' in datos:
            usuario.Email = datos['Email']
        if 'NombreUsuario' in datos:
            usuario.NombreUsuario = datos['NombreUsuario']
        if 'Direccion' in datos:
            usuario.Direccion = datos['Direccion']
        if 'IdLocalidad' in datos:
            usuario.IdLocalidad = valor_localidad
        if 'Telefono' in datos:
            usuario.Telefono = datos['Telefono']

        db.session.commit()
        return usuario

    return None

# def cambiar_password(id, nueva_password):
#     usuario = Usuario.query.filter_by(Id=id).first()
#     if usuario:
#         usuario.Password = generate_password_hash(nueva_password)
#         db.session.commit()
#         return True
#     return False
