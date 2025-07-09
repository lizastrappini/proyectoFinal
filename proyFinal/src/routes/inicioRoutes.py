from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/inicio')
def index():
    id = session.get('user', {}).get('Id')
    usuario = usuarioController.getUsuarioById(id)
    return render_template('inicio/index.html', usuario = usuario)

@inicio_bp.route('/')
def login():
    return render_template('usuario/index.html')