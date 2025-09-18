# app.py

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import inspect
import enum

from flask import Flask, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from config import DevelopmentConfig, app_configs
from src import db
from src.controllers import deportistaController, notificacionController
from src.models.parametro import Parametro
from src.models.usuario import Usuario
from src.routes.usuarioRoutes import usuario_bp
from src.routes.calendarioRoutes import calendario_bp
from src.routes.pagoRoutes import pago_bp
from src.routes.misPagosRoutes import mispago_bp
from src.routes.inicioRoutes import inicio_bp
from src.routes.entrenadorRoutes import entrenador_bp
from src.routes.deportistaRoutes import deportista_bp
from src.routes.estadisticasRoutes import estadisticas_bp
from src.routes.notificacionRoutes import notificacion_bp
from src.routes.contactoRoutes import contacto_bp
from src.routes.chatbotRoutes import chatbot_bp
from src.routes.faqRoutes import faq_bp
from src.utils.Mail import mail

app = Flask(__name__)
# Carga la configuración desde config.Config
app.config.from_object(app_configs['development'])

# Inicializa la extensión de base de datos
db.init_app(app)

# Registra tus blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(calendario_bp)
app.register_blueprint(pago_bp, url_prefix='/pago')
app.register_blueprint(mispago_bp, url_prefix='/mipago')
app.register_blueprint(inicio_bp)
app.register_blueprint(entrenador_bp, url_prefix='/entrenador')
app.register_blueprint(deportista_bp, url_prefix='/deportista')
app.register_blueprint(notificacion_bp, url_prefix='/notificacion')
app.register_blueprint(contacto_bp, url_prefix='/contacto')
app.register_blueprint(faq_bp, url_prefix='/faq')
app.register_blueprint(estadisticas_bp)  # monta en /estadisticas
app.register_blueprint(chatbot_bp)


# Context processor para exponer todos los Enum y funciones de src.utils.enums
@app.context_processor
def inject_enums_and_functions():
    items = {}
    import src.utils.enums as enums_module
    for name, obj in inspect.getmembers(enums_module):
        if inspect.isclass(obj) and issubclass(obj, enum.Enum):
            items[name] = obj
        elif callable(obj) and not name.startswith('_'):
            items[name] = obj
    return items

# Setup de Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'usuario_bp.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Inicializa el envío de mail
mail.init_app(app)

# Context processor para notificaciones globales
@app.context_processor
def inject_notificaciones():
    if current_user.is_authenticated:
        notificaciones = notificacionController.obtener_notificaciones()
    else:
        notificaciones = []
    return {'notificaciones': notificaciones}

# Context processor para datos de contacto y fecha actual
@app.context_processor
def inject_contacto_and_now():
    contacto = Parametro.query.first()
    return {'contacto': contacto, 'now': datetime.now()}

scheduler = BackgroundScheduler()
# Se ejecuta todos los días a la medianoche
scheduler.add_job(deportistaController.actualizar_categorias_automaticas, 'cron',month=1,day=1, hour=0, minute=0)
scheduler.start()
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=True)
