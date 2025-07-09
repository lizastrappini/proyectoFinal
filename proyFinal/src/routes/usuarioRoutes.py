from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import session
import src.utils.enums.generalEnum  as generalEnum
from flask_login import logout_user, login_required, current_user, login_user


usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/listar_usuarios', methods=['POST'])
def login():
    email = request.form.get('email-username')  
    password = request.form.get('password') 
    usuario = usuarioController.loginUser(email, password)
    if(usuario is not None):   
        login_user(usuario)
        flash("Bienvenido!", "success")
        return render_template('inicio/index.html', usuario=usuario)
    else:
        flash("Usuario o contraseña incorrectos","danger")
        return render_template('usuario/index.html')

@usuario_bp.route('/miCuenta', methods=['GET'])
def miCuenta():
    id = current_user.Id
    usuario = usuarioController.miCuenta(id)
    if(usuario is not None):   
        return render_template('usuario/cuenta.html', usuario=usuario)
    else:
        return render_template('iusuario/index.html', error='Usuario o contraseña incorrectos')

@usuario_bp.route('/editUsuario', methods=['POST'])
def editUsuario():
    id = current_user.Id
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


@login_required
@usuario_bp.route('/logout')
def logout():
    logout_user()  
    return render_template('usuario/index.html')
