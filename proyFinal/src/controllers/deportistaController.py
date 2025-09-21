from datetime import date
from flask import current_app, render_template, url_for
from flask_mail import Message
from src.controllers.usuarioController import enviar_mail_categoria
from src.models import usuario
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, FederadoEnum, RamaEnum
from src import db
from src.utils.Mail import mail

def obtener_deportistas(categoria=None, division=None, rama=None , dni=None):
    query = Usuario.query.filter_by(IdRol=2)

    if categoria:
        try:
            categoria_valor = int(categoria)
            query = query.filter_by(IdCategoria=str(categoria_valor))
        except KeyError:
            return []
    
    if division:
        try:
            division_valor = int(division)
            query = query.filter_by(IdDivision=str(division_valor))
        except KeyError:
            return []
        
    if rama:
        try:
            rama_valor = int(rama)
            query = query.filter_by(IdRama=str(rama_valor))
        except KeyError:
            return []
    if dni:
        query = query.filter(Usuario.Dni == int(dni))

    deportistas = []
    for e in query.all():
        try:
            cat_enum = CategoriaEnum(int(e.IdCategoria))
            categoria_nombre = cat_enum.name 
        except (ValueError, KeyError):
            categoria_nombre = 'Desconocido'

        try:
            est_enum = EstadoEnum(int(e.IdEstado))
            estado_nombre = est_enum.name
        except (ValueError, KeyError):
            estado_nombre = 'Desconocido'
            
        try:
            rama_enum = RamaEnum(int(e.IdRama))
            rama_nombre = rama_enum.name
        except (ValueError, KeyError):
            rama_nombre = 'Desconocido'
            
        try:
            division_enum = DivisionEnum(int(e.IdDivision))
            division_nombre = division_enum.name
        except (ValueError, KeyError):
            division_nombre = 'Desconocido'
        try:
            fed_enum = FederadoEnum(int(e.Federado)) if e.Federado is not None else None
            fed_nombre = fed_enum.name 
        except (ValueError, KeyError):
            fed_nombre = 'Desconocido'

            

        deportistas.append({
            'dni': e.Dni,
            'nombre': e.Nombre,
            'apellido': e.Apellido,
            'email': e.Email,
            'telefono': e.Telefono,
            'fechaNacimiento': e.FechaNacimiento.strftime('%d/%m/%Y') if e.FechaNacimiento else None,
            'fechaNacimientoISO': e.FechaNacimiento.strftime('%Y-%m-%d') if e.FechaNacimiento else None,
            'categoria': categoria_nombre,
            'rama': rama_nombre,
            'division': division_nombre,
            'estado': estado_nombre,
            'federado': fed_nombre
        })

    return deportistas

def getUsuarioById(id):
    return Usuario.query.filter_by(Id=id).first()


def agregarDeportista(nuevoDeportista):
    db.session.add(nuevoDeportista)
    db.session.commit()
    return nuevoDeportista

def actualizar_deportista(deportista):
    db.session.commit()
    
def obtener_deportista_por_dni(dni):
    return Usuario.query.filter_by(Dni=dni, IdRol=2).first()


def borrar_deportista(deportista):
    db.session.delete(deportista)
    db.session.commit()
    # return jsonify({'success': True, 'message': 'Entrenador eliminado'})
    
def enviar_mail_alta_deportista(deportista, password):
    if not deportista.Email:
        print("[ERROR] El deportista no tiene correo electrónico.")
        return False

    msg = Message(
        subject="Voley App - Bienvenida",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[deportista.Email]
    )
    link = f"http://127.0.0.1:5002" # aca despues va la url del servidor
    
    # link = url_for('usuarios.login', _external=True)
    msg.html = render_template("deportista/emailAlta.html", deportista=deportista, password=password, link=link)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo al deportista: {e}")
        return False
    
    
def calcular_categoria_por_fecha(fecha_nacimiento):
    
    if not fecha_nacimiento:
        # Si no hay fecha, devolver "NoDefinido" o el valor que uses
        return generalEnum.CategoriaEnum.NoEspecificada.value
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    # - (
    #     (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    # )

    if edad <= 12:
        return CategoriaEnum.Sub12.value
    elif edad <= 13:
        return CategoriaEnum.Sub13.value
    elif edad <= 14:
        return CategoriaEnum.Sub14.value
    elif edad <= 16:
        return CategoriaEnum.Sub16.value
    elif edad <= 18:
        return CategoriaEnum.Sub18.value
    elif edad <= 21:
        return CategoriaEnum.Sub21.value
    else:
        return CategoriaEnum.Primera.value


def actualizar_categorias_automaticas():
    hoy = date.today()
    usuarios = Usuario.query.all()
    
    for u in usuarios:
        if u.FechaNacimiento:
            u.IdCategoria = calcular_categoria_por_fecha(u.FechaNacimiento)
        else:
            u.IdCategoria = generalEnum.CategoriaEnum.NoEspecificada.value
    
    db.session.commit()