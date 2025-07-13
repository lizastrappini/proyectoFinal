from flask import Blueprint, redirect, request, render_template,flash, jsonify
from src.controllers import entrenadorController
import src.utils.enums.generalEnum as generalEnum



entrenador_bp = Blueprint('entrenador', __name__)


@entrenador_bp.route('/')
def index():
    categorias = [
    {'value': cat.name, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    return render_template('entrenador/index.html', categorias=categorias)


@entrenador_bp.route('/filtrar')
def filtrar():
    categoria = request.args.get('categoria')
    data = entrenadorController.obtener_entrenadores(categoria)
    return jsonify({'data': data})


@entrenador_bp.route('/addEntrenador', methods=['POST'])
def add_entrenador():
    dni = request.form.get('modalEditUserDNI')
    nombre = request.form.get('modalEditUserFirstName')
    apellido = request.form.get('modalEditUserLastName')
    categorias = request.form.getlist('select2Multiple')  # Esto es un array porque es multiple

    errores = []

    if not dni:
        errores.append('El campo DNI es obligatorio.')
    if not nombre:
        errores.append('El campo Nombre es obligatorio.')
    if not apellido:
        errores.append('El campo Apellido es obligatorio.')
    if not categorias:
        errores.append('Debe seleccionar al menos una categoría.')

    if errores:
        for error in errores:
            flash(error, 'danger')
        # return redirect('/entrenador')
    entrenadorController.agregar_entrenador(request.form)
    flash('Entrenador agregado exitosamente', 'success')
    return redirect('/entrenador')
