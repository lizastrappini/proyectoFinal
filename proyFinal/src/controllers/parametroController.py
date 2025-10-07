
from flask import current_app, render_template
from flask_mail import Message
from src import db
from src.utils.Mail import mail




def actualizar_parametro(parametro):
    db.session.commit()
    
def enviar_mail_actualizacion(deportistas,cuota):
    enviados = 0

    emails = {
        "laradelcoro01@gmail.com",
        "lizastrappini99@gmail.com",
        "morakopech@gmail.com",
        "laradelcoro01+3@gmail.com"
    }

    for deportista in deportistas:
        if not deportista.Email:
            continue

        if deportista.Email not in emails:
            continue

        msg = Message(
            subject="Voley App - Actualización de Cuota",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[deportista.Email]
        )
        msg.html = render_template("pago/actualizoCuota.html", deportista=deportista, cuota=cuota.Valor)

        try:
            mail.send(msg)
            enviados += 1
        except Exception as e:
            print(f"[ERROR] No se pudo enviar el correo a {deportista.Email}: {e}")

    return enviados