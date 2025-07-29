from babel.dates import format_date
from flask import Blueprint, redirect, request, render_template,flash, url_for
from sqlalchemy import desc
import src.controllers.usuarioController as usuarioController
from flask import session
from src.models.pago import Pago
from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from flask_login import logout_user, login_required, current_user, login_user
from src import db

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/listar_usuarios', methods=['POST'])
def login():
    email = request.form.get('email-username')  
    password = request.form.get('password') 
    usuario = usuarioController.loginUser(email, password)
    # remember = True if request.form.get('remember') == 'on' else False  
    usuario = usuarioController.loginUser(email, password)
    
    if(usuario is not None):   
        login_user(usuario) 
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
   
    if usuario is not None:
        pagos = db.session.query(Pago).filter_by(Usuario_id=id).order_by(desc(Pago.FechaPago)).all()

        datos_pagos = []
        for pago in pagos:
            try:
                est_enum = generalEnum.EstadoPagoEnum(int(pago.Estado))
                estado_nombre = est_enum.name
            except (ValueError, KeyError):
                estado_nombre = 'Desconocido'
            periodo = format_date(pago.FechaPago, "MMMM yyyy", locale="es_AR")
            datos_pagos.append({
                "fecha_pago": pago.FechaPago,
                "estado": estado_nombre,
                "periodo": periodo.capitalize()
            })
        return render_template('usuario/cuenta.html', usuario=usuario, pagos=datos_pagos)
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
     


@login_required   
@usuario_bp.route('/cambiar_contraseña', methods=['POST'])
def cambiar_contraseña():
    nueva = request.form.get('newPassword')
    confirmar = request.form.get('confirmPassword')

    errors = {}

    if not nueva or len(nueva) < 8:
        errors['newPassword'] = 'La contraseña debe tener al menos 8 caracteres.'
    if nueva != confirmar:
        errors['confirmPassword'] = 'Las contraseñas no coinciden.'

    if errors:
        usuario = usuarioController.miCuenta(current_user.Id)
        return render_template('usuario/cuenta.html', usuario=usuario, errors=errors)

    exito = usuarioController.actualizar_contraseña(current_user.Id, nueva)

    if exito:
        flash('Contraseña actualizada correctamente.', 'success')
    else:
        flash('Ocurrió un error al cambiar la contraseña.', 'danger')

    return redirect(url_for('usuarios.miCuenta'))
