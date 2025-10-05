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
from flask import jsonify, render_template
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
    if not usuario:
        return None

    def enum_name(enum_class, valor, default="No completado"):
        if valor is None:
            return default
        try:
            # Si es numérico, lo convierto
            valor_int = int(valor)
            return enum_class(valor_int).name
        except (ValueError, TypeError):
            # Si no, busco por nombre directo (si guardaste el nombre en la DB)
            try:
                return enum_class[valor].name
            except (KeyError, TypeError):
                return default
            
    return {
        'id': usuario.Id,
        'dni': usuario.Dni,
        'nombre': usuario.Nombre,
        'apellido': usuario.Apellido,
        'email': usuario.Email,
        'password': usuario.Password,
        'usuario': usuario.NombreUsuario,
        'idCategoria': enum_name(generalEnum.CategoriaEnum, usuario.IdCategoria),
        'localidad': enum_name(generalEnum.LocalidadEnum, usuario.Localidad),
        'localidad_valor': usuario.Localidad or 0,
        'estado': enum_name(generalEnum.EstadoEnum, usuario.IdEstado),
        'direccion': usuario.Direccion if usuario.Direccion else "-",
        'telefono': usuario.Telefono,
        'rol': enum_name(generalEnum.RolEnum, usuario.IdRol),
        'idEstado': usuario.IdEstado,
        'idRol': usuario.IdRol,
        'federado': enum_name(generalEnum.FederadoEnum, usuario.Federado),
        'fechaNacimiento': usuario.FechaNacimiento.strftime('%d/%m/%Y') if usuario.FechaNacimiento else None,
        'fechaNacimientoISO': usuario.FechaNacimiento.strftime('%Y-%m-%d') if usuario.FechaNacimiento else None,
    }



def actualizar_usuario(usuario):
    db.session.commit()

def getUsuarioById(id):
    return Usuario.query.filter_by(Id=id).first()




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
        Usuario.Federado == 1,
        Usuario.IdEstado == 1,
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