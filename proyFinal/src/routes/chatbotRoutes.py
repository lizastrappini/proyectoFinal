from functools import reduce
from operator import or_
from flask import Blueprint, request, jsonify

from src.models.pregunta import Pregunta


chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    pregunta_usuario = data.get('pregunta', '').strip()

    if not pregunta_usuario:
        return jsonify({'respuesta': "Por favor, escribí tu pregunta."})

    palabras = [p for p in pregunta_usuario.split() if p]

    filtros = []
    for palabra in palabras:
        # filtros.append(Pregunta.Pregunta.ilike(f"%{palabra}%"))
        filtros.append(Pregunta.PalabrasClave.ilike(f"%{palabra}%"))

    if not filtros:
        return jsonify({'respuesta': "Lo siento, no encontré una respuesta a tu pregunta."})

    # Creamos el OR de todos los filtros
    filtros_or = reduce(lambda x, y: or_(x, y), filtros)
    resultados = Pregunta.query.filter(filtros_or).all()

    if resultados:
        # Elegimos la FAQ con más coincidencias de palabras clave
        palabra_set = set(p.lower() for p in palabras)

        def coincidencias(faq):
            claves = set(k.lower() for k in faq.PalabrasClave.split(','))
            return len(palabra_set & claves)

        resultado = max(resultados, key=coincidencias)
        respuesta = resultado.Respuesta
    else:
        respuesta = "Lo siento, no encontré una respuesta a tu pregunta. ¿Podés reformularla?"

    return jsonify({'respuesta': respuesta})