from flask import Blueprint, render_template, redirect, url_for, request
from ..models import Paciente, db

patient_routes = Blueprint('patient_routes', __name__)

@patient_routes.route('/patients')
def list_patients():
    patients = Paciente.query.all()
    return render_template('patient/list_patients.html', patients=patients)
