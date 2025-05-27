from config import config
from src import init_app
from flask import Flask
from flask import render_template,redirect



app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login/index.html')


@app.route('/inicio')
def index():
    return render_template('inicio/index.html')

@app.route('/calendario')
def calendario():
    return render_template('inicio/calendario.html')

@app.route('/cuenta/pagos')
def cuenta():
    return render_template('inicio/cuenta.html')


@app.route('/pagos')
def pago():
    return render_template('inicio/pago.html')

@app.route('/deportistas')
def dedortista():
    return render_template('inicio/deportista.html')

@app.route('/entrenadores')
def entrenador():
    return render_template('inicio/entrenador.html')

@app.route('/estadisticas')
def estadistica():
    return render_template('inicio/estadistica.html')

@app.route('/restaurarContraseña')
def contraseña():
    return render_template('login/forgot-password.html')

if __name__=='__main__':
    app.run(debug=True)
    
    