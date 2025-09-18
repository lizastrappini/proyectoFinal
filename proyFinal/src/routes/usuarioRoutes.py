from datetime import date, datetime
import string
from babel.dates import format_date
from flask import Blueprint, redirect, request, render_template,flash, url_for
from sqlalchemy import Date, cast, desc
import src.controllers.usuarioController as usuarioController
from flask import session
from src.models.pago import Pago
from src.models.usuario import Usuario
import src.utils.enums.generalEnum  as generalEnum
from flask_login import logout_user, login_required, current_user, login_user
from src import db
from datetime import date
from sqlalchemy import and_


usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/listar_usuarios', methods=['GET'])
@login_required
def listar_usuarios():
    usuario = current_user
    cuota_al_dia = usuarioController.usuario_tiene_cuota_al_dia(usuario.Id)
    return render_template('inicio/index.html', usuario=usuario, cuota_al_dia=cuota_al_dia)

@usuario_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')  
    password = request.form.get('password') 
    usuario = usuarioController.loginUser(username, password)

    if usuario:
        login_user(usuario, remember = True) 
        flash("Bienvenido!", "success")
        return redirect(url_for('usuarios.listar_usuarios'))
       
    else:
        flash("Usuario o contraseña incorrectos", "danger")
        return render_template('usuario/index.html')


    
@usuario_bp.route('/cuota_al_dia', methods=['GET'])
@login_required
def cuota_al_dia_route():
    cuota = usuarioController.usuario_tiene_cuota_al_dia(current_user.Id)
    return {"cuota_al_dia": cuota}



@login_required
@usuario_bp.route('/miCuenta', methods=['GET'])
def miCuenta():
    id = current_user.Id
    usuario = usuarioController.miCuenta(id)
    localidades = [
    {'value': loc.value, 'text': loc.name}
    for loc in generalEnum.LocalidadEnum
    ]
    categorias = [
    {'value': cat.value, 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    if usuario is not None:
        pagos = db.session.query(Pago).filter_by(IdUsuario=id).order_by(desc(Pago.FechaPago)).all()

        datos_pagos = []
        for pago in pagos:
            try:
                est_enum = generalEnum.EstadoPagoEnum(int(pago.IdEstado))
                estado_nombre = est_enum.name
            except (ValueError, KeyError):
                estado_nombre = 'Desconocido'
            periodo = format_date(pago.FechaPago, "MMMM yyyy", locale="es_AR")
            datos_pagos.append({
                "fecha_pago": pago.FechaPago,
                "estado": estado_nombre,
                "periodo": periodo.capitalize()
            })
        return render_template('usuario/cuenta.html', usuario=usuario, pagos=datos_pagos, categorias= categorias,localidades=localidades)
    else:
        return render_template('usuario/index.html')


@login_required
@usuario_bp.route('/editUsuario', methods=['POST'])
def editUsuario():
    
    
    id = current_user.Id
    usuarioModel = {
        'Nombre': request.form.get('nombre'),
        'Apellido': request.form.get('apellido'),
        'Email': request.form.get('email'),
        'Direccion': request.form.get('direccion'),
        'Localidad': request.form.get('localidad'),
        'Telefono': request.form.get('telefono'),
        'Categoria': request.form.get('categoria'),
    }

    usuario = usuarioController.getUsuarioById(id)

    if(usuario is not None):   
        usuarioController.update(id, usuarioModel)
        usuario = usuarioController.miCuenta(id)
        localidades = [
            {'value': loc.value, 'text': loc.name}
            for loc in generalEnum.LocalidadEnum
            ]
        categorias = [
            {'value': cat.value, 'text': cat.name}
            for cat in generalEnum.CategoriaEnum
            ]
        return render_template('usuario/cuenta.html', usuario=usuario, categorias=categorias, localidades=localidades)
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
    

    if not password or len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "danger")
        return render_template('usuario/nuevaPass.html', token=token)
      
    elif not any(c.isupper() for c in password):
        flash("La contraseña debe contener al menos una letra mayúscula.", "danger")
        return render_template('usuario/nuevaPass.html', token=token)
       
    # Validación: al menos un símbolo
    elif not any(c in string.punctuation for c in password):
        flash("La contraseña debe contener al menos un símbolo (por ejemplo: !, @, #, etc).", "danger")
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
        # errors['newPassword'] = 'La contraseña debe tener al menos 8 caracteres.'
        flash("La contraseña debe tener al menos 8 caracteres.", "danger")
        return redirect(url_for('usuarios.miCuenta'))
    elif not any(c.isupper() for c in nueva):
        errors['newPassword'] = 'La contraseña debe contener al menos una letra mayúscula.'
    # Validación: al menos un símbolo
    elif not any(c in string.punctuation for c in nueva):
        errors['newPassword'] = 'La contraseña debe contener al menos un símbolo (por ejemplo: !, @, #, etc).'
    
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
