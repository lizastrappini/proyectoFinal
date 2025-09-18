from flask import Blueprint, request, jsonify
from flask_login import login_required
from src.models.pregunta import Pregunta  # Tu tabla FAQ
from src import db

chatbot_bp = Blueprint("chatbot", __name__)

# 1) Obtener lista de temas (DISTINCT)
@chatbot_bp.route("/chatbot/temas", methods=["GET"])
@login_required
def obtener_temas():
    temas = db.session.query(Pregunta.Tema).distinct().all()
    temas_lista = [t[0] for t in temas]  # [(“Pagos”,), (“Eventos”,)] -> ["Pagos", "Eventos"]
    return jsonify({"temas": temas_lista})


# 2) Obtener preguntas de un tema
@chatbot_bp.route("/chatbot/preguntas", methods=["GET"])
@login_required
def obtener_preguntas():
    tema = request.args.get("tema")
    if not tema:
        return jsonify({"preguntas": []})

    preguntas = Pregunta.query.filter_by(Tema=tema).all()
    data = [{"id": p.Id, "pregunta": p.Pregunta, "respuesta": p.Respuesta} for p in preguntas]
    return jsonify({"preguntas": data})


# 3) (Opcional) Obtener la respuesta de una pregunta puntual por id
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
