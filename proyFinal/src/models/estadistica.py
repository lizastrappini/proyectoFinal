from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ArchivoEstadistica(db.Model):
    __tablename__ = 'archivos_estadisticas'

    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    ruta_archivo = db.Column(db.String(255), nullable=False)
    
    