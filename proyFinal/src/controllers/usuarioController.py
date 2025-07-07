from src.models.usuario import Usuario

def loginUser(email,password):
    usuario = Usuario.query.filter_by(email=email, password=password).first()
    existe = usuario is not None  
    return existe

