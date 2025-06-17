from flask import Blueprint, render_template

doctor_bp = Blueprint('doctor', __name__, template_folder='templates', static_folder='static')

@doctor_bp.route('/doctor', methods=['GET'])
def doctor():
    return render_template('doctor/doctor.html')
