from src import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario'
    Id = db.Column(db.Integer, primary_key=True)
    Dni = db.Column(db.Integer)
    Nombre = db.Column(db.String(50))
    Apellido = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Password = db.Column(db.String(255))
    NombreUsuario = db.Column(db.String(50), unique=True, nullable=False)
    IdCategoria = db.Column(db.Integer, nullable=True)
    IdRama = db.Column(db.Integer, nullable=True)
    IdDivision = db.Column(db.Integer, nullable=True)
    Localidad = db.Column(db.String(10), nullable=True)
    IdEstado = db.Column(db.Integer)
    Direccion = db.Column(db.String(50))
    Telefono = db.Column(db.String(50))
    IdRol = db.Column(db.Integer)
    Token = db.Column(db.String(50))
    TokenEnviado = db.Column(db.Boolean, default=False)
    FechaVencimientoToken = db.Column(db.DateTime)
    FechaNacimiento = db.Column(db.DateTime, nullable=True)
    Federado = db.Column(db.Integer, nullable=True)
    CategoriaExtra = db.Column(db.String(30), nullable=True)
    


    def get_id(self):
        return str(self.Id)