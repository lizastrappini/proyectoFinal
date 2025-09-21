from src import db
from src.models.usuario import Usuario

class Pago(db.Model):
    __tablename__ = 'Pago'
    Id = db.Column(db.Integer, primary_key=True)
    IdEstado = db.Column(db.Integer, nullable=False)
    FechaVencimiento = db.Column(db.DateTime)
    FechaPago = db.Column(db.DateTime, nullable=True)
    Importe = db.Column(db.Numeric(16,2))
    Comprobante = db.Column(db.String(255), nullable=True)
    # FechaAlta = db.Column(db.DateTime, nullable=False)

    

    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.Id'), nullable=False)
    usuario= db.relationship('Usuario', backref= 'pagos')
    

    def get_id(self):
        return str(self.Id)