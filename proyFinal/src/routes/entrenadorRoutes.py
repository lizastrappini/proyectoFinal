from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum

entrenador_bp = Blueprint('entrenador', __name__)



@entrenador_bp.route('/entrenadores')
def index():
    return render_template('entrenador/index.html')