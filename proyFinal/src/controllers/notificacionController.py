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

"""
def obtener_notificaciones():
    if not current_user.is_authenticated:
        return []
    
    # Parámetros de filtro NUEVO
    palabra = request.args.get('buscar', '').lower()
    categoria = request.args.get('categoria')
    division = request.args.get('division')
    rama = request.args.get('rama')

    # Filtrar según el rol
    if current_user.IdRol in (1, 3):  # Admin o Entrenador
        resultados = Notificacion.query.all()
    else:  # Deportista
        resultados = Notificacion.query.filter(
            or_(
                Notificacion.IdCategoria == current_user.IdCategoria,
                Notificacion.IdCategoria == None
            )
        )#.all()
        
    # Filtro por palabra (en título o descripción)
    if palabra:
        query = query.filter(
            or_(
                Notificacion.Titulo.ilike(f"%{palabra}%"),
                Notificacion.Descripcion.ilike(f"%{palabra}%")
            )
        )

    # Filtro por categoría
    if categoria:
        query = query.filter(Notificacion.IdCategoria == int(categoria))

    # Filtro por división
    if division:
        query = query.filter(Notificacion.IdDivision == int(division))

    # Filtro por rama
    if rama:
        query = query.filter(Notificacion.IdRama == int(rama))

    resultados = query.all()

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
            'rama': nombre_rama
        })

    return notificaciones

# def getUsuarioById(id):
#     return Usuario.query.filter_by(Id=id).first()
"""



def obtener_notificaciones():
    if not current_user.is_authenticated:
        return []

    # Arrancamos query base según rol
    if current_user.IdRol in (1, 3):  # Admin o Entrenador
        query = Notificacion.query
    else:  # Deportista → filtrar por su categoría, rama y división
        query = Notificacion.query.filter(
            and_(
                or_(
                    Notificacion.IdCategoria == current_user.IdCategoria,
                    Notificacion.IdCategoria == None
                ),
                or_(
                    Notificacion.IdRama == current_user.IdRama,
                    Notificacion.IdRama == None
                ),
                or_(
                    Notificacion.IdDivision == current_user.IdDivision,
                    Notificacion.IdDivision == None
                )
            )
        )

    # --- FILTROS DEL FRONT ---
    buscar = request.args.get('buscar', '').strip()
    categoria = request.args.get('categoria', '').strip()
    division = request.args.get('division', '').strip()
    rama = request.args.get('rama', '').strip()

    if buscar:
        like_pattern = f"%{buscar}%"
        query = query.filter(
            or_(
                Notificacion.Titulo.ilike(like_pattern),
                Notificacion.Descripcion.ilike(like_pattern)
            )
        )

    if categoria and categoria.isdigit():
        query = query.filter(Notificacion.IdCategoria == int(categoria))

    if division and division.isdigit():
        query = query.filter(Notificacion.IdDivision == int(division))

    if rama and rama.isdigit():
        query = query.filter(Notificacion.IdRama == int(rama))
    
    # 👉 Ordenar y limitar a 6
    resultados = query.order_by(Notificacion.Id.desc()).limit(6).all()

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
    
