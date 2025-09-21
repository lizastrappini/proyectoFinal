import datetime
from flask import current_app, render_template, url_for
from flask_login import current_user
from flask_mail import Message
import pytz

from src.models.pago import Pago
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, EstadoPagoEnum, RamaEnum, RolEnum
from src import db
from src.utils.Mail import mail
from sqlalchemy import or_, and_

def obtener_pagos(estado= None, fecha_desde=None, fecha_hasta=None):
    query = Pago.query

    if current_user.IdRol == RolEnum.Deportista:
        query = query.filter(Pago.IdUsuario == current_user.Id)
    if estado is not None and estado != "":
        try:
            estado_valor = int(estado)
            query = query.filter(Pago.IdEstado == estado_valor)
        except ValueError:
            return []
        
    # Filtrar por fecha desde
    if fecha_desde:
        fecha_desde_dt = datetime.datetime.strptime(fecha_desde, "%Y-%m-%d")
        query = query.filter(
            or_(
                and_(Pago.FechaPago != None, Pago.FechaPago >= fecha_desde_dt),
                and_(Pago.FechaPago == None, Pago.FechaVencimiento >= fecha_desde_dt)
            )
        )

    # Filtrar por fecha hasta
    if fecha_hasta:
        fecha_hasta_dt = datetime.datetime.strptime (fecha_hasta, "%Y-%m-%d")
        query = query.filter(
            or_(
                and_(Pago.FechaPago != None, Pago.FechaPago <= fecha_hasta_dt),
                and_(Pago.FechaPago == None, Pago.FechaVencimiento <= fecha_hasta_dt)
            )
        )
    
    resultados = query.all()
    pagos = []
    
    for e in resultados:

        try:
            est_enum = EstadoPagoEnum(int(e.IdEstado))
            estado_nombre = est_enum.name
        except (ValueError, KeyError):
            estado_nombre = 'Desconocido'
            

        deportista = e.usuario
        deportista_nombre = f"{deportista.Nombre} {deportista.Apellido}" if deportista else "Sin asignar"

        pagos.append({
            'id': e.Id,
            'fechaVencimiento': e.FechaVencimiento.strftime('%d/%m/%Y') if e.FechaVencimiento else None,
            'fechaPago': e.FechaPago.strftime('%d/%m/%Y') if e.FechaPago else None,
            'fechaVencimientoISO': e.FechaVencimiento.strftime('%Y-%m-%d') if e.FechaVencimiento else None,
            'fechaPagoISO': e.FechaPago.strftime('%Y-%m-%d') if e.FechaPago else None,
            'importe': e.Importe,
            'estado': estado_nombre,
            'deportista': f"#{deportista.Id} {deportista_nombre}",
            'deportista_id': e.IdUsuario,
            'comprobante': 'Cargado' if e.Comprobante and e.Comprobante.strip() != '' else 'No Cargado',
            'comprobanteFoto': e.Comprobante

        })

    return pagos


def agregarPago(nuevoPago):
    db.session.add(nuevoPago)
    db.session.commit()
    return nuevoPago

def actualizar_pago(pago):
    db.session.commit()
    

def obtener_pago_por_id(id):
     return Pago.query.filter_by(Id=id).first()

def borrar_pago(pago):
    db.session.delete(pago)
    db.session.commit()
 
 
def enviar_recordatorios_cuotas():
    enviados = 0
    arg = pytz.timezone("America/Argentina/Buenos_Aires")
    hoy = datetime.now(arg).date()

    # Buscar pagos vencidos sin fecha de pago y que no estén marcados como Pagados
    pagos_vencidos = (
        Pago.query
        .filter(
            Pago.FechaVencimiento < hoy,
            Pago.FechaPago.is_(None),
            Pago.IdEstado != generalEnum.EstadoPagoEnum.Pago.value
        )
        .all()
    )

    for pago in pagos_vencidos:
        deportista = Usuario.query.get(pago.IdUsuario)
        if enviar_recordatorio_individual(deportista, pago):
            enviados += 1
    
    print(f"[INFO] Recordatorios enviados: {enviados}")
    return enviados

def enviar_recordatorio_individual(deportista, pago):
    if not deportista or not deportista.Email:
        return False
    
    msg = Message(
        subject="Voley App - Recordatorio de Cuota Vencida",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[deportista.Email]
    )
    msg.html = render_template(
        "pago/recordatorioCuota.html",
        deportista=deportista,
        fecha_venc=pago.FechaVencimiento.strftime("%d/%m/%Y")
    )

    try:
        mail.send(msg)
        print(f"[INFO] Email enviado a {deportista.Email}")
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo a {deportista.Email}: {e}")
        return False