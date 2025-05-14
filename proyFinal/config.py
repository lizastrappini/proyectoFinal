from decouple import config


class Config():
    SECRET_KEY = config('SECRET_KEY', default='clave_por_defecto')


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}