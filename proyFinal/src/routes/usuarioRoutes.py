from flask import Blueprint, redirect, request, render_template,flash, url_for
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
    remember = True if request.form.get('remember') == 'on' else False  
    usuario = usuarioController.loginUser(email, password)
    
    if(usuario is not None):   
        login_user(usuario, remember=remember) 
        flash("Bienvenido!", "success")
        return render_template('inicio/index.html', usuario=usuario)
    else:
        flash("Usuario o contraseña incorrectos","danger")
        return render_template('usuario/index.html')

@login_required
@usuario_bp.route('/miCuenta', methods=['GET'])
def miCuenta():
    id = current_user.Id
    usuario = usuarioController.miCuenta(id)
    if(usuario is not None):   
        return render_template('usuario/cuenta.html', usuario=usuario)
    else:
        return render_template('usuario/index.html')

@login_required
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
        'Categoria': request.form.get('Categoria'),
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

@usuario_bp.route('/ingresarEmailPass', methods=['GET'])
def ingresarEmailPass():  
    return render_template('usuario/forgot-password.html')
    
@usuario_bp.route('/recuperarPass', methods=['POST'])
def recuperarPass():
    email = request.form.get('email')  
    token = usuarioController.verificarTokenEnviado(email)
    if token is not None:
        return render_template('usuario/nuevaPass.html', token=token)
    
    email = usuarioController.enviarMailRecuperarPass(email)
    if(email is not None):   
        return render_template('usuario/recuperarPass.html', email=email)
    

@usuario_bp.route('/ingresarNuevaPass', methods=['GET'])
def ingresarNuevaPass():
    token = request.args.get('token')
    recuperar = usuarioController.recuperar_contraseña(token)
    if recuperar is None:
        flash("Token inválido o expirado", "danger")
        return render_template('usuario/forgot-password.html')
    else:
        return render_template('usuario/nuevaPass.html', token=token)
    

@usuario_bp.route('/cambiarPass', methods=['POST'])
def cambiarPass():
    token = request.form.get('token')
    password = request.form.get('password')
    confirmarPassword = request.form.get('confirmarPassword')
    yaUsada = usuarioController.verificarPass(token, password)

    if yaUsada is True:
        flash("La contraseña ya ha sido utilizada", "danger")
        return render_template('usuario/nuevaPass.html', token=token)

    if password != confirmarPassword:
        flash("Las contraseñas no coinciden", "danger")
        return render_template('usuario/nuevaPass.html', token=token)
    
    recuperar = usuarioController.cambiarContraseña(token, password)

    if recuperar is True:
        flash("Contraseña cambiada", "success")
        return render_template('usuario/index.html')
 
    else:
        flash("Ocurrio un error", "danger")
        return render_template('usuario/index.html')

