from flask import Blueprint, request, render_template,flash, redirect, url_for
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum
from flask_login import current_user
from flask_login import login_required
from src.utils.enums.generalEnum import RolEnum

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/inicio')
def index():
    if current_user.is_authenticated:
        return render_template('usuario/index.html')
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