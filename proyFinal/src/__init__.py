from flask import app
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


db = SQLAlchemy()


app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)  # duración del "recordarme"
