from operator import or_
from flask import current_app, render_template, url_for
from flask_login import current_user
from flask_mail import Message
from src.models.notificacion import Notificacion
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, RamaEnum
from src import db
from src.utils.Mail import mail

def obtener_notificaciones():
    if not current_user.is_authenticated:
        return []

    # Filtrar según el rol
    if current_user.IdRol in (1, 3):  # Admin o Entrenador
        resultados = Notificacion.query.all()
    else:  # Deportista
        resultados = Notificacion.query.filter(
            or_(
                Notificacion.Categoria == current_user.Categoria,
                Notificacion.Categoria == None
            )
        ).all()

    notificaciones = []
    for e in resultados:
        nombre_categoria = CategoriaEnum(int(e.Categoria)).name if e.Categoria is not None else "Todas"
        notificaciones.append({
            'id': e.Id,
            'titulo': e.Titulo,
            'descripcion': e.Descripcion,
            'categoria': nombre_categoria   
        })

    return notificaciones

# def getUsuarioById(id):
#     return Usuario.query.filter_by(Id=id).first()


def agregarNotificacion(nuevaNotif):
    db.session.add(nuevaNotif)
    db.session.commit()
    return nuevaNotif

# def actualizar_deportista(deportista):
#     db.session.commit()
    
def obtener_notif_por_id(id):
    return Notificacion.query.filter_by(Id=id).first()


def borrar_notificacion(notif):
    db.session.delete(notif)
    db.session.commit()
    # return jsonify({'success': True, 'message': 'Entrenador eliminado'})
    
def enviar_mail(destinatario,titulo,descripcion):
    if not destinatario:
        print("[ERROR] El usuario no tiene correo electrónico.")
        return False

    msg = Message(
        subject="Voley App - Notificación",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[destinatario]
    )
    link = f"http://127.0.0.1:5002/notificacion" # aca despues va la url del servidor
    
    # link = url_for('usuarios.login', _external=True)
    # msg.html = render_template("notificacion/emailNotif.html", titulo=titulo, descripcion=descripcion)
    msg.html = render_template(
        "notificacion/emailNotif.html",
        notificacion={'Titulo': titulo, 'Descripcion': descripcion},
        link=link
    )
    try:
        mail.send(msg)
        return True
    
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo al deportista: {e}")
        return False