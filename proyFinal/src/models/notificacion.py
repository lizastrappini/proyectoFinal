from src import db

class Notificacion(db.Model):
    __tablename__ = 'Notificacion'
    Id = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(50), nullable=False)
    Descripcion = db.Column(db.Text, nullable=True)
    IdCategoria = db.Column(db.Integer, nullable=True)
    IdDivision = db.Column(db.Integer, nullable=True)
    IdRama = db.Column(db.Integer, nullable=True)
    FechaEnvio = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Notificacion {self.Titulo}>"