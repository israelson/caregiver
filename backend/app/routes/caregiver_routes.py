from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import Profissional, db

caregiver_routes = Blueprint('caregiver_routes', __name__)

@caregiver_routes.route('/dashboard')
@login_required
def caregiver_dashboard():
    if current_user.role != 'caregiver':
        return redirect(url_for('auth_routes.login'))
    return render_template('caregiver/dashboard.html')

@caregiver_routes.route('/register')
def caregiver_register():
    return render_template('caregiver/register.html')

@caregiver_routes.route('/register', methods=['POST'])
def create_caregiver():
    data = request.form
    new_caregiver = Profissional(
        nome=data['nome'],
        cpf=data['cpf'],
        email=data['email'],
        telefone=data['telefone'],
        especializacoes=data['especializacoes'],
        disponibilidade=data['disponibilidade'],
        certificacoes=data['certificacoes'],
        fk_endereco=data['fk_endereco'],
        foto=data['foto']
    )
    db.session.add(new_caregiver)
    db.session.commit()
    return redirect(url_for('caregiver_routes.caregiver_register'))
