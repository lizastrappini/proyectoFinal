from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum

pago_bp = Blueprint('pagos', __name__)


@pago_bp.route('/pagos')
def index():
    return render_template('pago/index.html')
