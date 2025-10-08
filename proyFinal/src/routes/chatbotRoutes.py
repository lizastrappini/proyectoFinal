import re
import unicodedata
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from src.models.pregunta import Pregunta  
from src import db

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot/temas", methods=["GET"])
@login_required
def obtener_temas():
    temas = db.session.query(Pregunta.Tema).distinct().all()
    temas_lista = [t[0] for t in temas]  # [(“Pagos”,), (“Eventos”,)] -> ["Pagos", "Eventos"]
    return jsonify({"temas": temas_lista})


@chatbot_bp.route("/chatbot/preguntas", methods=["GET"])
@login_required
def obtener_preguntas():
    tema = request.args.get("tema")
    if not tema:
        return jsonify({"preguntas": []})
    preguntas = Pregunta.query.filter(
        Pregunta.Tema == tema,
        (Pregunta.Rol == current_user.IdRol) | (Pregunta.Rol == None)
     ).all()
    data = [{"id": p.Id, "pregunta": p.Pregunta, "respuesta": p.Respuesta} for p in preguntas]
    return jsonify({"preguntas": data})


@chatbot_bp.route("/chatbot/respuesta", methods=["GET"])
@login_required
def obtener_respuesta():
    pregunta_id = request.args.get("id")
    if not pregunta_id:
        return jsonify({"respuesta": "Pregunta no encontrada."})

    pregunta = Pregunta.query.get(pregunta_id)
    if not pregunta:
        return jsonify({"respuesta": "Pregunta no encontrada."})

    return jsonify({"respuesta": pregunta.Respuesta})




def limpiar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.lower()

@chatbot_bp.route("/chatbot", methods=["POST"])
@login_required
def procesar_pregunta():
    data = request.get_json()
    pregunta_usuario = limpiar_texto(data.get("pregunta", ""))

    if not pregunta_usuario:
        return jsonify({"respuesta": "No entendí tu pregunta, probá elegir un tema 👇"})

    preguntas = Pregunta.query.all()
    mejor_coincidencia = None
    max_matches = 0

    for p in preguntas:
        claves = [limpiar_texto(k) for k in (p.PalabrasClave or "").split(",")]

        matches = sum(1 for clave in claves if clave in pregunta_usuario)
        if matches > max_matches:
            max_matches = matches
            mejor_coincidencia = p

    if mejor_coincidencia:
        return jsonify({"respuesta": mejor_coincidencia.Respuesta})
    else:
        return jsonify({"respuesta": None})