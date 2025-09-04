from src import db

class EstadisticaUsuarioPartido(db.Model):
    __tablename__ = 'EstadisticaUsuarioPartido'
    Id = db.Column(db.Integer, primary_key=True)
    IdEstadisticaPorPartido = db.Column(db.Integer, nullable=False)
    IdUsuario = db.Column(db.Integer, nullable=False)
  

    def get_id(self):
        return str(self.Id)