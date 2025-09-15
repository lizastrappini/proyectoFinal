from src import db

class Parametro(db.Model):
    __tablename__ = 'Parametro'
    Id = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(50), nullable=False)
    Valor = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Parametro {self.Titulo}>"