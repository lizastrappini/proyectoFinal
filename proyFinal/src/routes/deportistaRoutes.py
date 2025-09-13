from datetime import datetime
import secrets
import string
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
import openpyxl
from src.controllers import deportistaController
from src.controllers.usuarioController import enviar_mail_categoria
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
    federados = [
    {'value': federado.value, 'text': federado.name}
    for federado in generalEnum.FederadoEnum
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
    return render_template('deportista/index.html', categorias=categorias,deportistas=lista_deportistas, ramas=ramas, divisiones=divisiones, federados= federados)


@deportista_bp.route('/filtrar')
def filtrar():
    categoria = request.args.get('categoria')
    division = request.args.get('division')
    rama = request.args.get('rama')
    dni = request.args.get('dni')
    
    if categoria and categoria.isdigit():
        categoria = int(categoria)
    
    if division and division.isdigit():
        division = int(division)
    
    if rama and rama.isdigit():
        rama = int(rama)
    
    data = deportistaController.obtener_deportistas(categoria=categoria,dni=dni,rama=rama, division=division) #agregar division=division
    return jsonify({'data': data})




@deportista_bp.route('/nuevoDeportista', methods=['POST'])
def agregar_deportista():
    try:
        dni = request.form.get('dni')
        if not dni or not dni.isdigit() or len(dni) != 8:
            raise ValueError("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        fechaNacimiento= request.form.get('fechaNacimiento')
        telefono = request.form.get('telefono')
        categoria_nombre = request.form.get('categoria')
        rama_nombre = request.form.get('rama')
        division_nombre = request.form.get('division')
        federado_nombre = request.form.get('federado')
        categoriaExtra = request.form.get('categoriaExtra')
        
        

        # Validar que categoria_nombre esté y sea válido
        if not categoria_nombre or categoria_nombre not in generalEnum.CategoriaEnum.__members__:
            raise ValueError("Categoría inválida o no seleccionada")
        
        if not categoriaExtra or categoriaExtra not in generalEnum.CategoriaEnum.__members__:
            raise ValueError("Categoría inválida o no seleccionada")
        
        if not rama_nombre or rama_nombre not in generalEnum.RamaEnum.__members__:
            raise ValueError("Rama inválida o no seleccionada")
        
        if not division_nombre or division_nombre not in generalEnum.DivisionEnum.__members__:
            raise ValueError("División inválida o no seleccionada")

        fecha_nacimiento_dt = datetime.strptime(fechaNacimiento, "%Y-%m-%d")  # Convertir string a datetime
        categoria_id = deportistaController.calcular_categoria_por_fecha(fecha_nacimiento_dt)
        # categoria_id = generalEnum.CategoriaEnum[categoria_nombre].value
        rama_id = generalEnum.RamaEnum[rama_nombre].value
        division_id = generalEnum.DivisionEnum[division_nombre].value
        categoriaExtraId = generalEnum.CategoriaEnum[categoriaExtra].value
        federado_id = generalEnum.FederadoEnum[federado_nombre].value
        caracteres = string.ascii_letters + string.digits  # letras + números
        password_plana = ''.join(secrets.choice(caracteres) for _ in range(8))  
        
        usuario_existente = Usuario.query.filter_by(Dni=dni).first()
        if usuario_existente:
         raise ValueError(f"Ya existe un usuario con el DNI {dni}")
     
        mail_usuario = Usuario.query.filter_by(Email=email).first()
        if mail_usuario:
         raise ValueError(f"Ya existe un usuario con el mismo email")

        nuevo_deportista = Usuario(
            Dni= dni,
            Nombre=nombre,
            Apellido=apellido,
            Email= email,
            FechaNacimiento= fechaNacimiento,
            IdCategoria = categoria_id,
            IdRama = rama_id,
            IdDivision = division_id,
            Password =  generate_password_hash(password_plana),
            # Password= generate_password_hash(password_plana),  # Contraseña aleatoria y hasheada
            NombreUsuario=f"{nombre}_{dni}",
            Localidad= 1,
            IdEstado=1,
            Direccion="N/A",
            Telefono=telefono,
            IdRol=2,
            Token=None,
            TokenEnviado=False,
            FechaVencimientoToken=None,
            Federado = federado_id,
            CategoriaExtra = categoriaExtraId
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
    try:
        nuevo_dni = request.form.get('dni')
        nuevo_email = request.form.get('email')
        
        if nuevo_dni and int(nuevo_dni) != dni:
            usuario_existente = Usuario.query.filter_by(Dni=nuevo_dni).first()
            if usuario_existente:
                raise ValueError(f"Ya existe un usuario con el DNI {nuevo_dni}")
        if not nuevo_dni or not nuevo_dni.isdigit() or len(nuevo_dni) != 8:
            raise ValueError("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")
        
        deportista = deportistaController.obtener_deportista_por_dni(dni)
        
        if not deportista:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Deportista no encontrado'}), 400
            else:
                flash('Deportista no encontrado', 'danger')
                return redirect(url_for('deportista.index'))
        
        if nuevo_email and nuevo_email != deportista.Email:
            email_usuario = Usuario.query.filter_by(Email=nuevo_email).first()
            if email_usuario:
                raise ValueError(f"Ya existe un usuario con el mismo email")
        
        categoria_vieja = deportista.IdCategoria
        
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        fechaNacimiento = request.form.get('fechaNacimiento')
        telefono = request.form.get('telefono')
        # nueva_cat = request.form.get('categoria')
        rama_nombre = request.form.get('rama')
        division_nombre = request.form.get('division')
        federado_nombre = request.form.get('federado')
        categoria_extra = request.form.get('categoriaExtra')
        

        # Actualiza campos
        deportista.Dni = nuevo_dni
        deportista.Nombre = nombre
        deportista.Apellido = apellido
        deportista.Email = nuevo_email
        deportista.FechaNacimiento = fechaNacimiento
        deportista.Telefono = telefono
        # deportista.IdCategoria = generalEnum.CategoriaEnum[categoria_nombre].value
        fecha_nacimiento_dt = datetime.strptime(fechaNacimiento, "%Y-%m-%d")
        deportista.IdCategoria = deportistaController.calcular_categoria_por_fecha(fecha_nacimiento_dt)
        deportista.IdRama = generalEnum.RamaEnum[rama_nombre].value
        deportista.IdDivision = generalEnum.DivisionEnum[division_nombre].value
        deportista.Federado = generalEnum.FederadoEnum[federado_nombre].value
        # deportista.CategoriaExtra = generalEnum.CategoriaEnum[categoria_extra].value
        deportista.CategoriaExtra = generalEnum.CategoriaEnum[categoria_extra].value
        
        
        if deportista.IdCategoria != categoria_vieja:
            enviar_mail_categoria(
                deportista.Email,
                deportista.Nombre,
                generalEnum.CategoriaEnum(deportista.IdCategoria).name
            )
        deportistaController.actualizar_deportista(deportista)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Deportista actualizado exitosamente'}), 200
        else:
            flash('Deportista actualizado exitosamente', 'success')
            return redirect(url_for('deportista.index'))

    except ValueError as ve:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': str(ve)}), 400
        else:
            flash(str(ve), 'danger')
            return redirect(url_for('deportista.index'))

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': f'Error inesperado: {str(e)}'}), 500
        else:
            flash('Ocurrió un error inesperado', 'danger')
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


# @deportista_bp.route('/subir_comprobante', methods=['POST'])
# def subir_comrpobante():
#     deportista = deportistaController.obtener_deportista_por_dni(dni)

#     if not deportista:
#         return jsonify({'success': False, 'message': 'Deportista no encontrado'}), 404

#     # Alternar estado
#     if int(deportista.IdEstado) == generalEnum.EstadoEnum.Activo:
#         deportista.IdEstado = generalEnum.EstadoEnum.Inactivo
#     else:
#         deportista.IdEstado = generalEnum.EstadoEnum.Activo

#     deportistaController.actualizar_deportista(deportista)

#     return jsonify({
#         'success': True,
#         'message': 'Estado actualizado',
#         'nuevo_estado': generalEnum.EstadoEnum(int(deportista.IdEstado)).name,
   
#     })



    