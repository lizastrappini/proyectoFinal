from flask import Blueprint, request, render_template,flash
import src.controllers.usuarioController as usuarioController
from flask import Blueprint, jsonify, request
import src.utils.enums.generalEnum as generalEnum

entrenador_bp = Blueprint('entrenador', __name__)

#ejemplo, hay que sacar de la base de datos
ENTRENADORES = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "categoria": "Sub 18",
        "fecha_ingreso": "2023-01-15",
    },
    {
        "nombre": "María",
        "apellido": "Gómez",
        "categoria": "Primera",
        "fecha_ingreso": "2022-08-20",
    },
    {
        "nombre": "Carlos",
        "apellido": "Lopez",
        "categoria": "Sub 21",
        "fecha_ingreso": "2023-03-01",
    }
]

@entrenador_bp.route('/')
def index():
    categorias = [
    {'value': cat.name.lower(), 'text': cat.name}
    for cat in generalEnum.CategoriaEnum
    ]
    return render_template('entrenador/index.html', categorias=categorias)

@entrenador_bp.route('/filtrar')
def filtrar():
    categoria = request.args.get('categoria')
    if categoria:
        data = [
            e for e in ENTRENADORES 
            if e['categoria'].replace(' ', '').lower() == categoria.replace(' ', '').lower()
        ]
    else:
        data = ENTRENADORES
    return jsonify({'data': data})
