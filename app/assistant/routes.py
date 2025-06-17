from flask import Blueprint, render_template

assistant_bp = Blueprint('assistant', __name__, template_folder='templates', static_folder='static')

@assistant_bp.route('/assistant', methods=['GET'])
def assistant():
    return render_template('assistant/assistant.html')
