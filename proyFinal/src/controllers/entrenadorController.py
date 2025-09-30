from flask import current_app, render_template, url_for
from flask_mail import Message
from sqlalchemy import or_
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, RamaEnum
from src import db
from src.utils.Mail import mail

def obtener_entrenadores(buscar=None):
    query = Usuario.query.filter_by(IdRol=3)
    if buscar:
        like_pattern = f"%{buscar}%"
        query = query.filter(
            or_(
                Usuario.Apellido.ilike(like_pattern),
                Usuario.Nombre.ilike(like_pattern),
                Usuario.Dni.ilike(like_pattern)
            )
        )
    entrenadores = []
    for e in query.all():
        try:
            cat_enum = CategoriaEnum(int(e.IdCategoria))
            categoria_nombre = cat_enum.name 
        except (ValueError, KeyError):
            categoria_nombre = 'Desconocido'
        # Division
        if e.IdDivision is not None:
            try:
                div_enum = DivisionEnum(int(e.IdDivision))
                division_nombre = div_enum.name
            except (ValueError, KeyError):
                division_nombre = "Desconocido"
        else:
            division_nombre = "-"

        # Rama
        if e.IdRama is not None:
            try:
                rama_enum = RamaEnum(int(e.IdRama))
                rama_nombre = rama_enum.name
            except (ValueError, KeyError):
                rama_nombre = "Desconocido"
        else:
            rama_nombre = "-"


        try:
            est_enum = EstadoEnum(int(e.IdEstado))
            estado_nombre = est_enum.name
        except (ValueError, KeyError):
            estado_nombre = 'Desconocido'

            

        entrenadores.append({
            'dni': e.Dni,
            'nombre': e.Nombre,
            'apellido': e.Apellido,
            'email': e.Email,
            'telefono': e.Telefono,
            'categoria': categoria_nombre,
            'division': division_nombre,
            'rama': rama_nombre,
            'estado': estado_nombre
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
    
def enviar_mail_alta_entrenador(entrenador, password):
    if not entrenador.Email:
        print("[ERROR] El entrenador no tiene correo electrónico.")
        return False

    msg = Message(
        subject="Voley App - Mensaje Bienvenida",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[entrenador.Email]
    )
    link = f"http://127.0.0.1:5002" # aca despues va la url del servidor
    
    # link = url_for('usuarios.login', _external=True)
    msg.html = render_template("entrenador/emailAlta.html", entrenador=entrenador, password=password, link=link)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo al entrenador: {e}")
        return False
    
