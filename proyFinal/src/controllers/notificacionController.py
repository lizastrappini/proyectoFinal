from sqlalchemy import or_, and_
from flask import current_app, render_template, url_for, request
from flask_login import current_user
from flask_mail import Message
from src.models.notificacion import Notificacion
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, RamaEnum
from src import db
from src.utils.Mail import mail



def obtener_notificaciones(buscar=None, categoria=None, division=None, rama=None):
    if not current_user.is_authenticated:
        return []

    query = Notificacion.query

    if current_user.IdRol == 2:  # Deportistas
        filtros = [Notificacion.FechaEnvio > current_user.FechaAlta]

        if current_user.IdCategoria is not None:
            filtros.append(or_(Notificacion.IdCategoria == current_user.IdCategoria,
                               Notificacion.IdCategoria == None))
        if current_user.IdRama is not None:
            filtros.append(or_(Notificacion.IdRama == current_user.IdRama,
                               Notificacion.IdRama == None))
        if current_user.IdDivision is not None:
            filtros.append(or_(Notificacion.IdDivision == current_user.IdDivision,
                               Notificacion.IdDivision == None))

        query = query.filter(and_(*filtros))

    if buscar:
        like_pattern = f"%{buscar}%"
        query = query.filter(
            or_(
                Notificacion.Titulo.ilike(like_pattern),
                Notificacion.Descripcion.ilike(like_pattern)
            )
        )
    if categoria is not None:
        query = query.filter(Notificacion.IdCategoria == categoria)
    if rama is not None:
        query = query.filter(Notificacion.IdRama == rama)
    if division is not None:
        query = query.filter(Notificacion.IdDivision == division)

    resultados = query.order_by(Notificacion.Id.desc()).all()

    notificaciones = []
    for e in resultados:
        nombre_categoria = CategoriaEnum(int(e.IdCategoria)).name if e.IdCategoria is not None else "Todas"
        nombre_division = DivisionEnum(int(e.IdDivision)).name if e.IdDivision is not None else "Todas"
        nombre_rama = RamaEnum(int(e.IdRama)).name if e.IdRama is not None else "Todas"

        notificaciones.append({
            'id': e.Id,
            'titulo': e.Titulo,
            'descripcion': e.Descripcion,
            'categoria': nombre_categoria,
            'division': nombre_division,
            'rama': nombre_rama,
            'fechaEnvio': e.FechaEnvio.strftime("%d/%m/%Y %H:%M")
        })

    return notificaciones


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
    link = f"http://127.0.0.1:5002/notificacion" 
    
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
    
