import secrets
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
from src.controllers import deportistaController, pagosController
from src.models.parametro import Parametro
from src.models.usuario import Usuario
from src.models.pago import Pago
from werkzeug.security import generate_password_hash

from src.utils.enums import generalEnum


contacto_bp = Blueprint('contacto', __name__)
# deportista_bp = Blueprint('deportista', __name__)


@contacto_bp.route('/')
def index():
  
    contactos = Parametro.query.all()

    # Convertirlos a un diccionario con clave = título (por ej: 'telefono') y valor = valor
    contacto_dict = {c.Titulo.lower(): c.Valor for c in contactos}

    return render_template('contacto/contacto.html', contacto=contacto_dict)


    
    


