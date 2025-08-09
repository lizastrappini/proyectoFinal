from decouple import config
import os
from datetime import timedelta

class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://usuarioapp:clave123@db:3306/proyecto_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY', default='clave_por_defecto')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'voleyapp@gmail.com' 
    MAIL_PASSWORD = 'rvniyvgqammziwiu'  # usar contraseña de aplicación en Gmail
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    REMEMBER_COOKIE_DURATION = timedelta(days=7)

class DevelopmentConfig(Config):
    DEBUG = True


app_configs = {
    'development': DevelopmentConfig
}