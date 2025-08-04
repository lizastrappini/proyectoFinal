# from flask import current_app, render_template, url_for
# from flask_mail import Message

# from src.models.pago import Pago
# from src.models.usuario import Usuario
# from src.utils.enums import generalEnum
# from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, EstadoPagoEnum, RamaEnum
# from src import db
# from src.utils.Mail import mail

# def obtener_pagos():
#     query = Pago.query
#     resultados = query.all()
#     pagos = []
#     for e in resultados:

#         try:
#             est_enum = EstadoPagoEnum(int(e.Estado))
#             estado_nombre = est_enum.name
#         except (ValueError, KeyError):
#             estado_nombre = 'Desconocido'
            
#         # nombre_apellido = "Sin asignar"
#         # if e.usuario:
#         #     nombre_apellido = f"{e.usuario.Nombre} {e.usuario.Apellido}"
#         deportista = e.usuario
#         deportista_nombre = f"{deportista.Nombre} {deportista.Apellido}" if deportista else "Sin asignar"

#         pagos.append({
#             'id': e.Id,
#             'fechaVencimiento': e.FechaVencimiento.strftime('%d/%m/%Y') if e.FechaVencimiento else None,
#             'fechaPago': e.FechaPago.strftime('%d/%m/%Y') if e.FechaPago else None,
#             'fechaVencimientoISO': e.FechaVencimiento.strftime('%Y-%m-%d') if e.FechaVencimiento else None,
#             'fechaPagoISO': e.FechaPago.strftime('%Y-%m-%d') if e.FechaPago else None,
#             'importe': e.Importe,
#             'estado': estado_nombre,
#             'deportista': deportista_nombre,
#             'deportista_id': e.Usuario_id
           
#         })

#     return pagos

# # def getUsuarioById(id):
# #     return Usuario.query.filter_by(Id=id).first()


# # def agregarPago(nuevoPago):
# #     db.session.add(nuevoPago)
# #     db.session.commit()
# #     return nuevoPago

# # def actualizar_pago(pago):
# #     db.session.commit()
    
# # # def obtener_pago_por_dni(dni):
# # #     return Pago.query.filter_by(Dni=dni, IdRol=2).first()
# # def obtener_pago_por_id(id):
# #      return Pago.query.filter_by(Id=id).first()

# # def borrar_pago(pago):
# #     db.session.delete(pago)
# #     db.session.commit()
#     # return jsonify({'success': True, 'message': 'Entrenador eliminado'})
    
# # def enviar_mail_alta_deportista(deportista, password):
# #     if not deportista.Email:
# #         print("[ERROR] El deportista no tiene correo electrónico.")
# #         return False

# #     msg = Message(
# #         subject="Voley App - Bienvenida",
# #         sender=current_app.config['MAIL_USERNAME'],
# #         recipients=[deportista.Email]
# #     )
# #     link = f"http://127.0.0.1:5002" # aca despues va la url del servidor
    
# #     # link = url_for('usuarios.login', _external=True)
# #     msg.html = render_template("deportista/emailAlta.html", deportista=deportista, password=password, link=link)

# #     try:
# #         mail.send(msg)
# #         return True
# #     except Exception as e:
# #         print(f"[ERROR] No se pudo enviar el correo al deportista: {e}")
# #         return False