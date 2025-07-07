from decouple import config
import os

class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://usuarioapp:clave123@db:3306/proyecto_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY', default='clave_por_defecto')


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}