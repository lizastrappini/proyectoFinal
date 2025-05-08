from flask import Flask,send_from_directory

# Routes
from .routes import AuthRoutes, IndexRoutes, LanguageRoutes

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(LanguageRoutes.main, url_prefix='/languages')

    return app

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('static', filename)