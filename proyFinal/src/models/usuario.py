from src import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario'
    Id = db.Column(db.Integer, primary_key=True)
    Dni = db.Column(db.Integer)
    Nombre = db.Column(db.String(50))
    Apellido = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Password = db.Column(db.String(50))
    NombreUsuario = db.Column(db.String(50))
    Categoria = db.Column(db.String(50), nullable=True)
    Rama = db.Column(db.String(50), nullable=True)
    Division = db.Column(db.String(50), nullable=True)
    Localidad = db.Column(db.String(10), nullable=True)
    IdEstado = db.Column(db.Integer)
    Direccion = db.Column(db.String(50))
    Telefono = db.Column(db.String(50))
    IdRol = db.Column(db.Integer)
    Token = db.Column(db.String(50))
    TokenEnviado = db.Column(db.Boolean, default=False)
    FechaVencimientoToken = db.Column(db.DateTime)
    


    def get_id(self):
        return str(self.Id)