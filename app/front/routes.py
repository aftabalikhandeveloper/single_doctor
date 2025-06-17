from flask import Blueprint, render_template

front_bp = Blueprint('front', __name__, template_folder='templates', static_folder='static')

@front_bp.route('/')
def home():
    return render_template('front/home.html')