from src import db
from flask_login import UserMixin

class Pregunta(db.Model):
    __tablename__ = 'faq'
    Id = db.Column(db.Integer, primary_key=True)
    Pregunta = db.Column(db.String(255), nullable=False)
    Respuesta = db.Column(db.Text, nullable=False)
    PalabrasClave = db.Column(db.String(255), nullable=False)
    Tema = db.Column(db.String(100), nullable=False) 
    Rol = db.Column(db.Integer, nullable= True)

    def get_id(self):
        return str(self.Id)