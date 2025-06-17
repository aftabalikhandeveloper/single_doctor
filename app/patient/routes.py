# using blueprint
from flask import Blueprint, render_template


patient_bp = Blueprint('patient', __name__, template_folder='templates', static_folder='static')


@patient_bp.route('/patient', methods=['GET'])
def patient():
    return render_template('patient/patient.html')