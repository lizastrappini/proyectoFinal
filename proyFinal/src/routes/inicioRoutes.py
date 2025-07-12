from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum
from flask_login import current_user

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/inicio')
def index():
    id = current_user.Id
    usuario = usuarioController.getUsuarioById(id)
    return render_template('inicio/index.html', usuario = usuario)

@inicio_bp.route('/')
def login():
    if current_user.is_authenticated:
        id = current_user.Id
        usuario = usuarioController.getUsuarioById(id)
        return render_template('inicio/index.html', usuario=usuario)
    else:
        return render_template('usuario/index.html')