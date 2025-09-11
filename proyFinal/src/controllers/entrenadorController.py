from flask import current_app, render_template, url_for
from flask_mail import Message
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum , EstadoEnum
from src import db
from src.utils.Mail import mail

def obtener_entrenadores(categoria=None, dni=None):
    query = Usuario.query.filter_by(IdRol=3)

    if categoria:
        try:
            categoria_valor = int(categoria)
            query = query.filter_by(IdCategoria=str(categoria_valor))
        except KeyError:
            return []
    if dni:
        query = query.filter(Usuario.Dni == int(dni))

    entrenadores = []
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

            

        entrenadores.append({
            'dni': e.Dni,
            'nombre': e.Nombre,
            'apellido': e.Apellido,
            'email': e.Email,
            'telefono': e.Telefono,
            'categoria': categoria_nombre,
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
        subject="Voley App - Bienvenida",
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
    
