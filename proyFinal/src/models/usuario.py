from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))