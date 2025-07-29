import secrets
import string
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
from src.controllers import deportistaController
from src.models.usuario import Usuario
from werkzeug.security import generate_password_hash

from src.utils.enums import generalEnum



deportista_bp = Blueprint('deportista', __name__)


@deportista_bp.route('/')
def index():
    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    ramas = [
    {'value': rama.value, 'text': rama.name}
    for rama in generalEnum.RamaEnum
    ]
    divisiones = [
    {'value': div.value, 'text': div.name}
    for div in generalEnum.DivisionEnum
    ]
    deportistas = deportistaController.obtener_deportistas()  
    lista_deportistas = [
        {
            'dni': e['dni'],
            'nombre': e['nombre'],
            'apellido': e['apellido']
        }
        for e in deportistas
    ]
    return render_template('deportista/index.html', categorias=categorias,deportistas=lista_deportistas, ramas=ramas, divisiones=divisiones)


@deportista_bp.route('/filtrar')
def filtrar():
    categoria = request.args.get('categoria')
    rama = request.args.get('rama')
    dni = request.args.get('dni')
    
    if categoria and categoria.isdigit():
        categoria = int(categoria)
    
    if rama and rama.isdigit():
        rama = int(rama)
    
    data = deportistaController.obtener_deportistas(categoria=categoria, dni=dni, rama=rama)
    return jsonify({'data': data})




@deportista_bp.route('/nuevoDeportista', methods=['POST'])
def agregar_deportista():
    try:
        dni = request.form.get('dni')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        categoria_nombre = request.form.get('categoria')
        rama_nombre = request.form.get('rama')
        division_nombre = request.form.get('division')

        # Validar que categoria_nombre esté y sea válido
        if not categoria_nombre or categoria_nombre not in generalEnum.CategoriaEnum.__members__:
            raise ValueError("Categoría inválida o no seleccionada")
        
        if not rama_nombre or rama_nombre not in generalEnum.RamaEnum.__members__:
            raise ValueError("Rama inválida o no seleccionada")
        
        if not division_nombre or division_nombre not in generalEnum.DivisionEnum.__members__:
            raise ValueError("División inválida o no seleccionada")


        categoria_id = generalEnum.CategoriaEnum[categoria_nombre].value
        rama_id = generalEnum.RamaEnum[rama_nombre].value
        division_id = generalEnum.DivisionEnum[division_nombre].value
        # password_plana = '12345678' # despues hay que generar una contraseña aleatoria y hasheada
        # Generar contraseña aleatoria segura
        caracteres = string.ascii_letters + string.digits  # letras + números
        password_plana = ''.join(secrets.choice(caracteres) for _ in range(8))  # 10 caracteres

        nuevo_deportista = Usuario(
            Dni= dni,
            Nombre=nombre,
            Apellido=apellido,
            Email= email,
            Categoria = categoria_id,
            Rama = rama_id,
            Division = division_id,
            Password =  generate_password_hash(password_plana),
            # Password= generate_password_hash(password_plana),  # Contraseña aleatoria y hasheada
            NombreUsuario=f"entrenador_{dni}",
            Localidad= 1,
            IdEstado=1,
            Direccion="N/A",
            Telefono=telefono,
            IdRol=2,
            Token=None,
            TokenEnviado=False,
            FechaVencimientoToken=None
        )
        deportistaController.agregarDeportista(nuevo_deportista)
        deportistaController.enviar_mail_alta_deportista(nuevo_deportista, password_plana)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Deportista creado exitosamente'}), 200
        else:
            flash('Deportista creado exitosamente', 'success')
            return redirect(url_for('deportista.index'))
    except Exception as e:
        mensaje_error = str(e)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': mensaje_error}), 400
        else:
            flash(f'Error al crear deportista: {mensaje_error}', 'danger')
            return redirect(url_for('deportista.index'))



@deportista_bp.route('/editar/<int:dni>', methods=['POST'])
def editar_deportista(dni):
    deportista = deportistaController.obtener_deportista_por_dni(dni)
    if not deportista:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Deportista no encontrado'}), 400
        else:
            flash('Deportista no encontrado', 'danger')
            return redirect(url_for('deportista.index'))

    dni = request.form.get('dni')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    categoria_nombre = request.form.get('categoria')
    rama_nombre = request.form.get('rama')
    division_nombre = request.form.get('division')
    

    # Actualiza campos
    deportista.Dni = dni
    deportista.Nombre = nombre
    deportista.Apellido = apellido
    deportista.Email = email
    deportista.Telefono = telefono
    deportista.Categoria = generalEnum.CategoriaEnum[categoria_nombre].value
    deportista.Rama = generalEnum.RamaEnum[rama_nombre].value
    deportista.Division = generalEnum.DivisionEnum[division_nombre].value
    

    deportistaController.actualizar_deportista(deportista)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Deportista actualizado exitosamente'}), 200
    else:
        flash('Deportista actualizado exitosamente', 'success')
        return redirect(url_for('deportista.index'))



@deportista_bp.route('/eliminar/<int:dni>', methods=['POST'])
def eliminar_deportista(dni):
    deportista = deportistaController.obtener_deportista_por_dni(dni)
    if not deportista:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Deportista no encontrado'}), 200
        else:
            flash('Deportista no encontrado', 'danger')
            return redirect(url_for('deportista.index'))
    
    deportistaController.borrar_deportista(deportista)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Entrenador eliminado'})
    else:
        flash('Deportista eliminado exitosamente', 'success')
        return redirect(url_for('deportista.index'))
    
    
@deportista_bp.route('/cambiarEstado/<int:dni>', methods=['POST'])
def cambiar_estado(dni):
    deportista = deportistaController.obtener_deportista_por_dni(dni)

    if not deportista:
        return jsonify({'success': False, 'message': 'Deportista no encontrado'}), 404

    # Alternar estado
    if int(deportista.IdEstado) == generalEnum.EstadoEnum.Activo:
        deportista.IdEstado = generalEnum.EstadoEnum.Inactivo
    else:
        deportista.IdEstado = generalEnum.EstadoEnum.Activo

    deportistaController.actualizar_deportista(deportista)

    return jsonify({
        'success': True,
        'message': 'Estado actualizado',
        'nuevo_estado': generalEnum.EstadoEnum(int(deportista.IdEstado)).name,
   
    })


