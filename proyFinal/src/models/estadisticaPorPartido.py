from src import db

class EstadisticaPorPartido(db.Model):
    __tablename__ = 'EstadisticaPorPartido'
    Id = db.Column(db.Integer, primary_key=True)
    IdPartido = db.Column(db.Integer, nullable=False)
    Fecha = db.Column(db.DateTime, nullable=False)
    IdContrincante = db.Column(db.Integer, nullable=False)
    IdCategoria = db.Column(db.Integer, nullable=False)
    IdRama = db.Column(db.Integer, nullable=False)
    IdDivision = db.Column(db.Integer, nullable=False)
    Resultado = db.Column(db.Integer, nullable=False)
    IdEntrenador = db.Column(db.Integer, nullable=False)
    FechaCarga = db.Column(db.DateTime, nullable=False)
    RutaArchivo = db.Column(db.String(255), nullable=True)

    def get_id(self):
        return str(self.Id)