from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/listar_usuarios', methods=['POST'])
def login():
    email = request.form.get('email-username')  
    password = request.form.get('password') 
    usuario = usuarioController.loginUser(email, password)
    if(usuario is not None):   
        session['user'] = {
                'Id': usuario.Id,
                'Email': usuario.Email,
                'IdRol': usuario.IdRol,
                'Rol': generalEnum.RolEnum(usuario.IdRol).name ,
                'Nombre': usuario.Nombre,
            }
        flash("Bienvenido!", "success")
        return render_template('inicio/index.html', usuario=usuario)
    else:
        flash("Usuario o contraseña incorrectos","danger")
        return render_template('usuario/index.html')

@usuario_bp.route('/miCuenta', methods=['GET'])
def miCuenta():
    id = session.get('user_id')
    usuario = usuarioController.miCuenta(id)
    if(usuario is not None):   
        return render_template('usuario/cuenta.html', usuario=usuario)
    else:
        return render_template('iusuario/index.html', error='Usuario o contraseña incorrectos')

@usuario_bp.route('/editUsuario', methods=['POST'])
def editUsuario():
    id = session.get('user_id') 
    usuarioModel = {
        'Nombre': request.form.get('Nombre'),
        'Apellido': request.form.get('Apellido'),
        'Email': request.form.get('Email'),
        'NombreUsuario': request.form.get('Usuario'),
        'Direccion': request.form.get('Direccion'),
        'Localidad': request.form.get('Localidad'),
        'Telefono': request.form.get('Telefono'),
    }

    usuario = usuarioController.getUsuarioById(id)

    if(usuario is not None):   
        usuarioController.update(id, usuarioModel)
        usuario = usuarioController.miCuenta(id)
        return render_template('usuario/cuenta.html', usuario=usuario)
    else:
        return render_template('usuario/index.html', error='Usuario o contraseña incorrectos')


@usuario_bp.route('/deportistas')
def deportistas():
    return render_template('inicio/deportista.html')