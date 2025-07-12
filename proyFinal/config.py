from decouple import config
import os

class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://usuarioapp:clave123@db:3306/proyecto_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY', default='clave_por_defecto')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'lizaotrascosas@gmail.com' #cambiar por voleyapp@gmail.com cuando nos deje usarlo
    MAIL_PASSWORD = 'pvbukucydnvgskye'  # usar contraseña de aplicación en Gmail
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}