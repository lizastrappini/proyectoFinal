from flask import Blueprint, request, render_template
import src.controllers.usuarioController as usuarioController

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/listar_usuarios', methods=['POST'])
def login():
    email = request.form.get('email-username')  
    password = request.form.get('password') 

    usuarios = usuarioController.loginUser(email, password)
    if(usuarios):   
        return render_template('inicio/calendario.html', usuarios=usuarios)
    else:
        return render_template('login/index.html', error='Usuario o contraseña incorrectos')


