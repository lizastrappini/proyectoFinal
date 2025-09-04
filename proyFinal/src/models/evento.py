from src import db

class Evento(db.Model):
    __tablename__ = 'Evento'
    Id = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(50), nullable=False)
    IdTipoEvento = db.Column(db.Integer, nullable=False)
    FechaInicio = db.Column(db.DateTime, nullable=False)
    FechaFin = db.Column(db.DateTime, nullable=False)
    TodoElDia = db.Column(db.Boolean, default=False)
    Localidad = db.Column(db.Integer, nullable=True)
    Descripcion = db.Column(db.Text, nullable=True)
    IdCategoria = db.Column(db.Integer, nullable=True)
    Contrincante = db.Column(db.Integer, nullable=True)
    

    
    def __repr__(self):
        return f"<Evento {self.Titulo}>"