# here in __init__.py to register the blueprints.

from flask import Flask
from app.front.routes import front_bp
from app.doctor.routes import doctor_bp
from app.patient.routes import patient_bp
from app.assistant.routes import assistant_bp


def create_app():
    app = Flask(__name__)

    # Register blueprints
    # home page is here
    app.register_blueprint(front_bp)
    # doctor, patient, and assistant pages are here
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(assistant_bp)


    # Set up configurations, database, etc. here if needed

    return app