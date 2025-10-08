from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from src import db
from src.models import parametro
from src.models.parametro import Parametro



parametro_bp = Blueprint('parametro', __name__)



@parametro_bp.route('/')
def parametro():
    parametros = Parametro.query.all() 
    return render_template('parametro/parametro.html', parametros=parametros)

@parametro_bp.route('/editarParametro', methods=['POST'])
def editarParametro():
    try:
        for key, value in request.form.items():
            parametro = Parametro.query.get(key)
            if parametro:
                parametro.Valor = value

        db.session.commit()
        flash("Parámetros actualizados correctamente", "success")
        return redirect(url_for('parametro.parametro'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar parámetros: {e}", "danger")
        return redirect(url_for('parametro.parametro'))
