import datetime
from src.controllers import deportistaController
from src.models.pago import Pago
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
from sqlalchemy import and_, cast, Date, or_, and_
from datetime import date


def loginUser(username, password):
    usuario = Usuario.query.filter_by(NombreUsuario=username).first()
    if usuario and check_password_hash(usuario.Password, password):
        return usuario
    return None

def miCuenta(id):
    usuario = Usuario.query.filter_by(Id=id).first()
    if(usuario is not None):
        localidad_valor = int(usuario.Localidad or 0)
        localidad_nombre = generalEnum.LocalidadEnum(localidad_valor).name
        categoria_valor = int(usuario.IdCategoria or 0)
        categoria_nombre = generalEnum.CategoriaEnum(categoria_valor).name
        return {
            'id': usuario.Id,
            'dni': usuario.Dni,
            'nombre': usuario.Nombre,
            'apellido': usuario.Apellido,
            'email': usuario.Email,
            'password': usuario.Password,
            'usuario': usuario.NombreUsuario,
            'idCategoria': categoria_nombre,
            'localidad': localidad_nombre,
            'localidad_valor' : localidad_valor,
            'estado': generalEnum.EstadoEnum(int(usuario.IdEstado)).name,
            'direccion': usuario.Direccion or 'No completado',
            'telefono': usuario.Telefono,
            'rol': generalEnum.RolEnum(usuario.IdRol).name ,
            'idEstado': usuario.IdEstado,
            'idRol': usuario.IdRol,
            'federado': generalEnum.FederadoEnum(usuario.Federado).name,
            'fechaNacimiento': usuario.FechaNacimiento.strftime('%d/%m/%Y') if usuario.FechaNacimiento else None,
            'fechaNacimientoISO': usuario.FechaNacimiento.strftime('%Y-%m-%d') if usuario.FechaNacimiento else None,
            
        }



def getUsuarioById(id):
    return Usuario.query.filter_by(Id=id).first()

def update(id, datos):
    usuario = Usuario.query.filter_by(Id=id).first()

    if usuario:
        # categoria_vieja = usuario.IdCategoria
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
        if 'Localidad' in datos:
            usuario.Localidad = datos['Localidad']
        if 'Telefono' in datos:
            usuario.Telefono = datos['Telefono']
    

        db.session.commit()
        # if usuario.IdCategoria != categoria_vieja:
        #     enviar_mail_categoria(
        #         usuario.Email,
        #         usuario.Nombre,
        #         generalEnum.CategoriaEnum(usuario.IdCategoria).name
        #     )

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
    link = f"http://127.0.0.1:5002/ingresarNuevaPass?token={token}"

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
    if usuario:
        usuario.Password = generate_password_hash(nueva_contraseña)
        usuario.Token = None
        usuario.TokenEnviado = False
        usuario.FechaVencimientoToken = None
        db.session.commit()
        return True
    return False


# def verificarPass(token,password):
#     usuario = Usuario.query.filter_by(Token=token).first()
#     if usuario:
#         if usuario.Password == password:
#             return True
#         else:
#             return False
#     return False

def verificarPass(token, password):
    usuario = Usuario.query.filter_by(Token=token).first()
    if usuario:
        return check_password_hash(usuario.Password, password)
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
            usuario.Password = generate_password_hash(nueva_contraseña)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al actualizar contraseña: {e}")
        db.session.rollback()
        return False
    
    

def usuario_tiene_cuota_al_dia(usuario_id):
    hoy = date.today()
    ultimo_pago = Pago.query.filter(
        and_(
            Pago.IdUsuario == usuario_id,
            Pago.IdEstado == 1,
            cast(Pago.FechaPago, Date) <= hoy
        )
    ).order_by(Pago.FechaPago.desc()).first()
    
    if ultimo_pago:
        return ultimo_pago.FechaPago.month == hoy.month and ultimo_pago.FechaPago.year == hoy.year

    return False

def enviar_mail_categoria(usuario_email, nombre, categoria_nueva):
    msg = Message(
        "Voley App - Actualización de Categoría",
        sender="lizaotrascosas@gmail.com",
        recipients=[usuario_email]
    )
    msg.html = render_template("usuario/emailCambioCategoria.html", nombre=nombre, categoria_nueva=categoria_nueva)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")
        return False
    
    
def getUsuarioByCategoriaYRama(categoria, rama, division, ids_seleccionados=None):
    try:
        cat_buscar = int(categoria)
    except Exception:
        return []

    query = Usuario.query.filter(
        Usuario.IdRama == rama,
        Usuario.IdDivision == division,
        or_(
            Usuario.IdCategoria == cat_buscar,
            and_(Usuario.CategoriaExtra.isnot(None), Usuario.CategoriaExtra != '')
        )
    )

    if ids_seleccionados:
        query = query.filter(Usuario.Id.in_(ids_seleccionados))

    usuarios = query.with_entities(
        Usuario.Id, Usuario.Nombre, Usuario.Apellido,
        Usuario.IdCategoria, Usuario.CategoriaExtra
    ).all()

    resultado = []
    for u in usuarios:
        user_id, nombre, apellido, id_categoria, categoria_extra = u

        if id_categoria == cat_buscar:
            resultado.append({"Id": user_id, "Nombre": f"{nombre} {apellido}"})
            continue


        if categoria_extra:
            partes = [p.strip() for p in categoria_extra.split(",") if p.strip() != ""]
            for p in partes:
                if p.isdigit() and int(p) == cat_buscar:
                    resultado.append({"Id": user_id, "Nombre": f"{nombre} {apellido}"})
                    break

    return resultado