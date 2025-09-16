import datetime
from flask import current_app, render_template, url_for
from flask_login import current_user
from flask_mail import Message

from src.models.pago import Pago
from src.models.usuario import Usuario
from src.utils.enums import generalEnum
from src.utils.enums.generalEnum import CategoriaEnum, DivisionEnum , EstadoEnum, EstadoPagoEnum, RamaEnum, RolEnum
from src import db
from src.utils.Mail import mail

def obtener_pagos(estado= None,  fecha_desde=None, fecha_hasta=None):
    query = Pago.query
    # 🔒 Filtrar por usuario si es deportista
    if current_user.IdRol == RolEnum.Deportista:
        query = query.filter(Pago.IdUsuario == current_user.Id)
    if estado:
        try:
            estado_valor = int(estado)
            query = query.filter_by(IdEstado=str(estado_valor))
        except KeyError:
            return []
        
    # Filtrar por fecha desde
    if fecha_desde:
        try:
            fecha_desde_dt = datetime.datetime.strptime(fecha_desde, "%Y-%m-%d")
            query = query.filter(Pago.FechaPago >= fecha_desde_dt)
        except ValueError:
            pass

    # Filtrar por fecha hasta
    if fecha_hasta:
        try:
            fecha_hasta_dt = datetime.datetime.strptime(fecha_hasta, "%Y-%m-%d")
            query = query.filter(Pago.FechaPago <= fecha_hasta_dt)
        except ValueError:
            pass
    
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
 