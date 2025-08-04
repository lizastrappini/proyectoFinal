from src import db
from src.models.usuario import Usuario

class Pago(db.Model):
    __tablename__ = 'Pago'
    Id = db.Column(db.Integer, primary_key=True)
    IdEstado = db.Column(db.Integer, nullable=False)
    FechaVencimiento = db.Column(db.DateTime)
    FechaPago = db.Column(db.DateTime)
    Importe = db.Column(db.Numeric(16,2))
    

    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.Id'), nullable=False)
    usuario= db.relationship('Usuario', backref= 'pagos')
    

    def get_id(self):
        return str(self.Id)