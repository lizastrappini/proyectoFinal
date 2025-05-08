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
    return render_template('inicio/calendario.html')

@app.route('/calendario')
def calendario():
    return render_template('inicio/calendario.html')

if __name__=='__main__':
    app.run(debug=True)
    