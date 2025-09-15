from functools import reduce
from operator import or_
from flask import Blueprint, render_template, request, jsonify

from src.models.pregunta import Pregunta


faq_bp = Blueprint('faq', __name__)



@faq_bp.route('/')
def faq():
    faqs = Pregunta.query.all() 
    return render_template('faq/faq.html', faqs=faqs)