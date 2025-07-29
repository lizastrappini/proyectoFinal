import secrets
import string
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
from src.controllers import entrenadorController
from src.models.usuario import Usuario
import src.utils.enums.generalEnum as generalEnum
from werkzeug.security import generate_password_hash



entrenador_bp = Blueprint('entrenador', __name__)


@entrenador_bp.route('/')
def index():
    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    entrenadores = entrenadorController.obtener_entrenadores()  
    lista_entrenadores = [
        {
            'dni': e['dni'],
            'nombre': e['nombre'],
            'apellido': e['apellido']
        }
        for e in entrenadores
    ]
    return render_template('entrenador/index.html', categorias=categorias,entrenadores=lista_entrenadores)


@entrenador_bp.route('/filtrar')
def filtrar():
    categoria = request.args.get('categoria')
    dni = request.args.get('dni')
    
    if categoria and categoria.isdigit():
        categoria = int(categoria)
    
    data = entrenadorController.obtener_entrenadores(categoria=categoria, dni=dni)
    return jsonify({'data': data})




@entrenador_bp.route('/nuevoEntrenador', methods=['POST'])
def agregar_entrenador():
    try:
        dni = request.form.get('dni')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        categoria_nombre = request.form.get('categoria')

        # Validar que categoria_nombre esté y sea válido
        if not categoria_nombre or categoria_nombre not in generalEnum.CategoriaEnum.__members__:
            raise ValueError("Categoría inválida o no seleccionada")

        categoria_id = generalEnum.CategoriaEnum[categoria_nombre].value
        # password_plana = '12345678' # despues hay que generar una contraseña aleatoria y hasheada
        # Generar contraseña aleatoria segura
        caracteres = string.ascii_letters + string.digits  # letras + números
        password_plana = ''.join(secrets.choice(caracteres) for _ in range(10))  # 10 caracteres


        nuevo_entrenador = Usuario(
            Dni= dni,
            Nombre=nombre,
            Apellido=apellido,
            Email= email,
            Categoria = categoria_id,
            Password =  generate_password_hash(password_plana),
            # Password= generate_password_hash(password_plana),  # Contraseña aleatoria y hasheada
            NombreUsuario=f"entrenador_{dni}",
            Localidad= 1,
            IdEstado=1,
            Direccion="N/A",
            Telefono=telefono,
            IdRol=3,
            Token=None,
            TokenEnviado=False,
            FechaVencimientoToken=None
        )
        entrenadorController.agregarEntrenador(nuevo_entrenador)
        entrenadorController.enviar_mail_alta_entrenador(nuevo_entrenador, password_plana)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Entrenador creado exitosamente'}), 200
        else:
            flash('Entrenador creado exitosamente', 'success')
            return redirect(url_for('entrenador.index'))
    except Exception as e:
        mensaje_error = str(e)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': mensaje_error}), 400
        else:
            flash(f'Error al crear entrenador: {mensaje_error}', 'danger')
            return redirect(url_for('entrenador.index'))



@entrenador_bp.route('/editar/<int:dni>', methods=['POST'])
def editar_entrenador(dni):
    entrenador = entrenadorController.obtener_entrenador_por_dni(dni)
    if not entrenador:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Entrenador no encontrado'}), 400
        else:
            flash('Entrenador no encontrado', 'danger')
            return redirect(url_for('entrenador.index'))

    dni = request.form.get('dni')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    categoria_nombre = request.form.get('categoria')

    # Actualiza campos
    entrenador.Dni = dni
    entrenador.Nombre = nombre
    entrenador.Apellido = apellido
    entrenador.Email = email
    entrenador.Telefono = telefono
    entrenador.Categoria = generalEnum.CategoriaEnum[categoria_nombre].value

    entrenadorController.actualizar_entrenador(entrenador)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Entrenador actualizado exitosamente'}), 200
    else:
        flash('Entrenador actualizado exitosamente', 'success')
        return redirect(url_for('entrenador.index'))



@entrenador_bp.route('/eliminar/<int:dni>', methods=['POST'])
def eliminar_entrenador(dni):
    entrenador = entrenadorController.obtener_entrenador_por_dni(dni)
    if not entrenador:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Entrenador no encontrado'}), 200
        else:
            flash('Entrenador no encontrado', 'danger')
            return redirect(url_for('entrenador.index'))
    
    entrenadorController.borrar_entrenador(entrenador)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Entrenador eliminado'})
    else:
        flash('Entrenador eliminado exitosamente', 'success')
        return redirect(url_for('entrenador.index'))
    
    
@entrenador_bp.route('/cambiarEstado/<int:dni>', methods=['POST'])
def cambiar_estado(dni):
    entrenador = entrenadorController.obtener_entrenador_por_dni(dni)

    if not entrenador:
        return jsonify({'success': False, 'message': 'Entrenador no encontrado'}), 404

    # Alternar estado
    if int(entrenador.IdEstado) == generalEnum.EstadoEnum.Activo:
        entrenador.IdEstado = generalEnum.EstadoEnum.Inactivo
    else:
        entrenador.IdEstado = generalEnum.EstadoEnum.Activo

    entrenadorController.actualizar_entrenador(entrenador)

    return jsonify({
        'success': True,
        'message': 'Estado actualizado',
        'nuevo_estado': generalEnum.EstadoEnum(int(entrenador.IdEstado)).name,
   
    })


