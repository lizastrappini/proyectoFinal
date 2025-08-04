from config import config
from flask import Flask, render_template, redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy 
from src import db
from src.controllers import notificacionController
from src.routes.usuarioRoutes import usuario_bp
from src.routes.calendarioRoutes import calendario_bp
from src.routes.pagoRoutes import pago_bp
from src.routes.inicioRoutes import inicio_bp
from src.routes.entrenadorRoutes import entrenador_bp
from src.routes.deportistaRoutes import deportista_bp
from src.routes.estadisticasRoutes import estadisticas_bp
from src.routes.notificacionRoutes import notificacion_bp

import src.utils.enums
import inspect
import enum
from flask_login import LoginManager, current_user
import src.controllers.usuarioController as usuarioController
from src.models.usuario import Usuario
from src.utils.Mail import mail

app = Flask(__name__)

app.config.from_object('config.Config')

# Inicializa SQLAlchemy
db.init_app(app)

# Registra blueprints (rutas)
app.register_blueprint(usuario_bp)
app.register_blueprint(calendario_bp)
app.register_blueprint(pago_bp, url_prefix='/pago')
app.register_blueprint(inicio_bp)
app.register_blueprint(entrenador_bp, url_prefix='/entrenador')
app.register_blueprint(deportista_bp, url_prefix='/deportista')
app.register_blueprint(notificacion_bp, url_prefix='/notificacion')
app.register_blueprint(estadisticas_bp)

#para exportar los enums a cualquier template
@app.context_processor
def inject_enums_and_functions():
    context_items = {}
    for name, obj in inspect.getmembers(src.utils.enums):
        if inspect.isclass(obj) and issubclass(obj, enum.Enum):
            context_items[name] = obj
    for name, obj in inspect.getmembers(src.utils.enums):
        if callable(obj) and not inspect.isclass(obj) and not name.startswith('_'):
            context_items[name] = obj

    return context_items


login_manager = LoginManager()
login_manager.login_view = 'usuario_bp.login' 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
  # ✅ importar desde config

mail.init_app(app)


@app.context_processor
def inject_notificaciones():
    if current_user.is_authenticated:
        notificaciones = notificacionController.obtener_notificaciones()
    else:
        notificaciones = []
    return dict(notificaciones=notificaciones)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=True)