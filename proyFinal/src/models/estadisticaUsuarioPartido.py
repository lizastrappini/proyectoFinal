from src import db

class EstadisticaUsuarioPartido(db.Model):
    __tablename__ = 'EstadisticaUsuarioPartido'
    Id = db.Column(db.Integer, primary_key=True)
    IdEstadisticaPorPartido = db.Column(db.Integer, nullable=False)
    IdUsuario = db.Column(db.Integer, nullable=False)
    #RECEPCION
    REE = db.Column(db.Integer, nullable=True)
    REV = db.Column(db.Integer, nullable=True)
    RE0 = db.Column(db.Integer, nullable=True)
    RE1 = db.Column(db.Integer, nullable=True)
    RE2 = db.Column(db.Integer, nullable=True)
    RE3 = db.Column(db.Integer, nullable=True)
    RETOTAL = db.Column(db.Integer, nullable=True)
    #ROTACION
    ROE = db.Column(db.Integer, nullable=True)
    ROB = db.Column(db.Integer, nullable=True)
    RO0 = db.Column(db.Integer, nullable=True)
    RO1 = db.Column(db.Integer, nullable=True)
    RO2 = db.Column(db.Integer, nullable=True)
    RO3 = db.Column(db.Integer, nullable=True)
    RO4 = db.Column(db.Integer, nullable=True)
    ROTOTAL = db.Column(db.Integer, nullable=True)
    #TRANSICION
    TRE = db.Column(db.Integer, nullable=True)
    TRB = db.Column(db.Integer, nullable=True)
    TR0 = db.Column(db.Integer, nullable=True)
    TR1 = db.Column(db.Integer, nullable=True)
    TR2 = db.Column(db.Integer, nullable=True)
    TR3 = db.Column(db.Integer, nullable=True)
    TR4 = db.Column(db.Integer, nullable=True)
    TRTOTAL = db.Column(db.Integer, nullable=True)
    #SAQUE
    SA0 = db.Column(db.Integer, nullable=True)
    SA1 = db.Column(db.Integer, nullable=True)
    SA2 = db.Column(db.Integer, nullable=True)
    SA3 = db.Column(db.Integer, nullable=True)
    SA4 = db.Column(db.Integer, nullable=True)
    SATOTAL = db.Column(db.Integer, nullable=True)
    #BLOQUEO
    BLP = db.Column(db.Integer, nullable=True)
    BLN = db.Column(db.Integer, nullable=True)
    BLTOTAL = db.Column(db.Integer, nullable=True)
    


    def get_id(self):
        return str(self.Id)