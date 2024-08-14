from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import Prontuario, Paciente, Profissional, db

record_routes = Blueprint('record_routes', __name__)

@record_routes.route('/fill_record/<int:paciente_id>')
@login_required
def fill_record(paciente_id):
    if current_user.role not in ['admin', 'caregiver']:
        return redirect(url_for('auth_routes.login'))
    
    paciente = Paciente.query.get(paciente_id)
    profissionais = Profissional.query.filter_by(status='aprovado').all()
    return render_template('record/fill_record.html', paciente=paciente, profissionais=profissionais)

@record_routes.route('/fill_record/<int:paciente_id>', methods=['POST'])
@login_required
def create_record(paciente_id):
    if current_user.role not in ['admin', 'caregiver']:
        return redirect(url_for('auth_routes.login'))
    
    data = request.form
    new_record = Prontuario(
        observacoes=data['observacoes'],
        fk_paciente=paciente_id,
        fk_profissional=current_user.id
    )
    db.session.add(new_record)
    db.session.commit()
    return redirect(url_for('record_routes.fill_record', paciente_id=paciente_id))
