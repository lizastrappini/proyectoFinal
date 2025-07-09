from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum

calendario_bp = Blueprint('calendario', __name__)

@calendario_bp.route('/calendario', methods=['GET'])
def index():
    return render_template('calendario/index.html')
    