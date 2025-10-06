import datetime
import secrets
import string
from flask import Blueprint, redirect, request, render_template,flash, jsonify, url_for
import pytz
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
    ramas = [
    {'value': rama.value, 'text': rama.name}
    for rama in generalEnum.RamaEnum
    ]
    divisiones = [
    {'value': div.value, 'text': div.name}
    for div in generalEnum.DivisionEnum
    ]

    return render_template('entrenador/index.html', categorias=categorias,  ramas=ramas, divisiones=divisiones)


@entrenador_bp.route('/filtrar')
def filtrar():

    buscar = request.args.get('buscar', '').strip()
    
    data = entrenadorController.obtener_entrenadores(buscar=buscar)
    return jsonify({'data': data})




@entrenador_bp.route('/nuevoEntrenador', methods=['POST'])
def agregar_entrenador():
    try:
        dni = request.form.get('dni')
        if not dni or not dni.isdigit() or len(dni) != 8:
            raise ValueError("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        categoria_nombre = request.form.get('categoria')
        rama_nombre = request.form.get('rama')
        division_nombre = request.form.get('division')
        categoriaExtra = request.form.getlist('categoriaExtra')
       
        
        if not categoria_nombre or categoria_nombre not in generalEnum.CategoriaEnum.__members__:
            raise ValueError("Categoría inválida o no seleccionada")

        if rama_nombre and rama_nombre in generalEnum.RamaEnum.__members__:
            rama_id = generalEnum.RamaEnum[rama_nombre].value
        else:
            rama_id = None

        if division_nombre and division_nombre in generalEnum.DivisionEnum.__members__:
            division_id = generalEnum.DivisionEnum[division_nombre].value
        else:
            division_id = None

     
         
        categoriaExtraIds = []
        if categoriaExtra:
            try:
                categoriaExtraIds = [
                    generalEnum.CategoriaEnum[nombre].value
                    for nombre in categoriaExtra
                    if nombre in generalEnum.CategoriaEnum.__members__
                ]
            except Exception:
                raise ValueError("Categoría Extra inválida")

        categoria_id = generalEnum.CategoriaEnum[categoria_nombre].value
        
        caracteres = string.ascii_letters + string.digits  
        password_plana = ''.join(secrets.choice(caracteres) for _ in range(10))  

        usuario_existente = Usuario.query.filter_by(Dni=dni).first()
        if usuario_existente:
         raise ValueError(f"Ya existe un usuario con el DNI {dni}")
     
     
        mail_usuario = Usuario.query.filter_by(Email=email).first()
        if mail_usuario:
         raise ValueError(f"Ya existe un usuario con el mismo email")

        arg = pytz.timezone("America/Argentina/Buenos_Aires")
        
        nuevo_entrenador = Usuario(
            Dni= dni,
            Nombre=nombre,
            Apellido=apellido,
            Email= email,
            IdCategoria = categoria_id,
            IdRama = rama_id,
            IdDivision = division_id,
            Password =  generate_password_hash(password_plana),
            NombreUsuario=f"{nombre}_{dni}",
            IdEstado=1,
            Telefono=telefono,
            IdRol=3,
            Token=None,
            TokenEnviado=False,
            FechaVencimientoToken=None,
            Federado = 3,
            CategoriaExtra = ",".join(map(str, categoriaExtraIds)) if categoriaExtraIds else None,
            FechaAlta = datetime.datetime.now(arg)
            
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
    try:
        nuevo_dni = request.form.get('dni')
        nuevo_email = request.form.get('email')
        categoria_extra = request.form.getlist('categoriaExtra')
        rama_nombre = request.form.get('rama')
        division_nombre = request.form.get('division')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        categoria_nombre = request.form.get('categoria')
      
        
        
        categoriaExtraIds = []
        if categoria_extra:
            try:
                categoriaExtraIds = [
                    generalEnum.CategoriaEnum[nombre].value
                    for nombre in categoria_extra
                    if nombre in generalEnum.CategoriaEnum.__members__
                ]
            except Exception:
                raise ValueError("Categoría Extra inválida")
        
        if nuevo_dni and int(nuevo_dni) != dni:
            usuario_existente = Usuario.query.filter_by(Dni=nuevo_dni).first()
            if usuario_existente:
                raise ValueError(f"Ya existe un usuario con el DNI {nuevo_dni}")
        if not nuevo_dni or not nuevo_dni.isdigit() or len(nuevo_dni) != 8:
            raise ValueError("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")
                    
        entrenador = entrenadorController.obtener_entrenador_por_dni(dni)
        
        if not entrenador:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Entrenador no encontrado'}), 400
            else:
                flash('Entrenador no encontrado', 'danger')
                return redirect(url_for('entrenador.index'))
        
        if nuevo_email and nuevo_email != entrenador.Email:
            email_usuario = Usuario.query.filter_by(Email=nuevo_email).first()
            if email_usuario:
                raise ValueError(f"Ya existe un usuario con el mismo email")
            

        if rama_nombre and rama_nombre in generalEnum.RamaEnum.__members__:
            entrenador.IdRama = generalEnum.RamaEnum[rama_nombre].value
        else:
            entrenador.IdRama = None
        
        if division_nombre and division_nombre in generalEnum.DivisionEnum.__members__:
            entrenador.IdDivision = generalEnum.DivisionEnum[division_nombre].value
        else:
            entrenador.IdDivision = None
            
        entrenador.Dni = nuevo_dni
        entrenador.Nombre = nombre
        entrenador.Apellido = apellido
        entrenador.Email = nuevo_email
        entrenador.Telefono = telefono
        entrenador.IdCategoria = generalEnum.CategoriaEnum[categoria_nombre].value
        entrenador.CategoriaExtra = ",".join(map(str, categoriaExtraIds)) if categoriaExtraIds else None
        

        entrenadorController.actualizar_entrenador(entrenador)
    
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Entrenador actualizado exitosamente'}), 200
        else:
            flash('Entrenador actualizado exitosamente', 'success')
            return redirect(url_for('entrenador.index'))
    except ValueError as ve:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': str(ve)}), 400
        else:
            flash(str(ve), 'danger')
            return redirect(url_for('entrenador.index'))

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': f'Error inesperado: {str(e)}'}), 500
        else:
            flash('Ocurrió un error inesperado', 'danger')
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


@entrenador_bp.route('/getEntrenador/<int:dni>', methods=['GET'])
def getEntrenador(dni):
    entrenador = entrenadorController.obtener_entrenador_por_dni(dni)

    if not entrenador:
        return jsonify({'error': 'Entrenador no encontrado'}), 404

    return jsonify({
        "dni": entrenador.Dni,
        "nombre": entrenador.Nombre,
        "apellido": entrenador.Apellido,
        "email": entrenador.Email,
        "telefono": entrenador.Telefono,
        "categoria": generalEnum.CategoriaEnum(entrenador.IdCategoria).name if entrenador.IdCategoria else None,
        "rama": generalEnum.RamaEnum(entrenador.IdRama).name if entrenador.IdRama else None,
        "division": generalEnum.DivisionEnum(entrenador.IdDivision).name if entrenador.IdDivision else None,
        "categoriaExtra": [
            generalEnum.CategoriaEnum(int(x)).name for x in entrenador.CategoriaExtra.split(",")
        ] if entrenador.CategoriaExtra else [],
        
    })
