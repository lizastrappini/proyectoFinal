import datetime
from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from src import db
from werkzeug.security import generate_password_hash
import secrets
import smtplib
from email.message import EmailMessage
from flask_mail import Message
from src.utils.Mail import mail
from datetime import datetime, timezone, timedelta
from flask import render_template
from werkzeug.security import check_password_hash

def loginUser(email,password):
    usuario = Usuario.query.filter_by(Email=email, Password=password).first() 
    return usuario
# def loginUser(email, password):
#     usuario = Usuario.query.filter_by(Email=email).first()
#     if usuario and check_password_hash(usuario.Password, password):
#         return usuario
#     return None

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
            'categoria': generalEnum.CategoriaEnum(int(usuario.Categoria)).name,
            'localidad': generalEnum.LocalidadEnum(usuario.IdLocalidad).name,
            'estado': generalEnum.EstadoEnum(int(usuario.IdEstado)).name,
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


def ocultar_email_parcial(email, porcentaje=0.60):
    if '@' not in email:
        return email

    usuario, dominio = email.split('@')
    longitud = len(usuario)
    cantidad_a_ocultar = int(longitud * porcentaje)

    parte_visible = usuario[:longitud - cantidad_a_ocultar]
    oculto = parte_visible + '*' * cantidad_a_ocultar

    return f"{oculto}@{dominio}"


def generar_token():
    return secrets.token_urlsafe(32)

def enviar_mail_recuperacion(email, token, nombre):
    link = f"http://127.0.0.1:5001/ingresarNuevaPass?token={token}"

    msg = Message("Voley App - Recuperación de contraseña",
                  sender="lizaotrascosas@gmail.com",
                  recipients=[email])
    msg.html = render_template("usuario/emailRecuperacion.html", nombre=nombre, link=link)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")
        return False


def enviarMailRecuperarPass(email):
    usuario = Usuario.query.filter_by(Email= email).first()
    if usuario:
        token = secrets.token_urlsafe(32)
        usuario.Token = token
        usuario.TokenEnviado = True
        usuario.FechaVencimientoToken = datetime.now(timezone.utc) + timedelta(hours=1)
        enviar_mail_recuperacion(usuario.Email, token, usuario.Nombre)
        db.session.commit()
        email = ocultar_email_parcial(usuario.Email)
        return email

    return None


def recuperar_contraseña(token):
    rec = Usuario.query.filter_by(Token=token, TokenEnviado=True).first()
    if not rec or rec.FechaVencimientoToken < datetime.now():
        return None
    return rec

def cambiarContraseña(token, nueva_contraseña):
    usuario = Usuario.query.filter_by(Token=token).first()
    usuario.Password = nueva_contraseña
    usuario.Token = None
    usuario.TokenEnviado = False
    usuario.FechaVencimientoToken = None
    db.session.commit()
    return True

def verificarPass(token,password):
    usuario = Usuario.query.filter_by(Token=token).first()
    if usuario:
        if usuario.Password == password:
            return True
        else:
            return False
    return False

def verificarTokenEnviado(email):
    usuario = Usuario.query.filter_by(Email = email).first()
    if usuario:
        if usuario.Token is not None and usuario.TokenEnviado is True:
            return usuario.Token
        else:
            return None
    return None


def actualizar_contraseña(usuario_id, nueva_contraseña):
    try:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.Password = nueva_contraseña
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al actualizar contraseña: {e}")
        db.session.rollback()
        return False