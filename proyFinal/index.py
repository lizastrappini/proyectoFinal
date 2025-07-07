from config import config
from flask import Flask, render_template,redirect
from flask_sqlalchemy import SQLAlchemy 

from src.models.usuario import db
from src.routes.usuarioRoutes import usuarios_bp

app = Flask(__name__)

app.config.from_object('config.Config')

# Inicializa SQLAlchemy
db.init_app(app)

# Registra blueprints (rutas)
app.register_blueprint(usuarios_bp)

@app.route('/')
def login():
    return render_template('login/index.html')


@app.route('/inicio')
def index():
    return render_template('inicio/index.html')

@app.route('/calendario')
def calendario():
    return render_template('inicio/calendario.html')

@app.route('/cuenta/pagos')
def cuenta():
    return render_template('inicio/cuenta.html')


@app.route('/pagos')
def pago():
    return render_template('inicio/pago.html')

@app.route('/deportistas')
def dedortista():
    return render_template('inicio/deportista.html')

@app.route('/entrenadores')
def entrenador():
    return render_template('inicio/entrenador.html')

@app.route('/estadisticas')
def estadistica():
    return render_template('inicio/estadistica.html')

@app.route('/restaurarContraseña')
def contraseña():
    return render_template('login/forgot-password.html')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)