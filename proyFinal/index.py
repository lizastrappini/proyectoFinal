from config import config
from flask import Flask, render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy 
from src import db
from src.routes.usuarioRoutes import usuario_bp
from src.routes.calendarioRoutes import calendario_bp
from src.routes.pagoRoutes import pago_bp
from src.routes.inicioRoutes import inicio_bp
from src.routes.entrenadorRoutes import entrenador_bp
import src.utils.enums
import inspect
import enum


app = Flask(__name__)

app.config.from_object('config.Config')

# Inicializa SQLAlchemy
db.init_app(app)

# Registra blueprints (rutas)
app.register_blueprint(usuario_bp)
app.register_blueprint(calendario_bp)
app.register_blueprint(pago_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(entrenador_bp)

#para exportar los enums a cualquier template
@app.context_processor
def inject_enums():
    enums_dict = {}
    for name, obj in inspect.getmembers(src.utils.enums):
        if inspect.isclass(obj) and issubclass(obj, enum.Enum):
            enums_dict[name] = obj
    return enums_dict

#en lugar de poner las rutas aca, las dividimos por funcionalidad en calendarioRoutes, usuarioRoutes, etc.
""" 
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
    return render_template('login/forgot-password.html') """
    

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=True)