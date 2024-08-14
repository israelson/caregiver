from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from app import db
from app.models import User, Profissional
from functools import wraps

admin_routes = Blueprint('admin_routes', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Você não tem permissão para acessar esta página.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_routes.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_routes.route('/approve_caregivers', methods=['GET'])
@login_required
@admin_required
def approve_caregivers():
    pending_caregivers = Profissional.query.filter_by(status='pendente').all()
    return render_template('admin/approve_caregivers.html', caregivers=pending_caregivers)

@admin_routes.route('/approve_caregiver/<int:caregiver_id>', methods=['POST'])
@login_required
@admin_required
def approve_caregiver(caregiver_id):
    caregiver = Profissional.query.get(caregiver_id)
    if caregiver:
        caregiver.status = 'aprovado'
        db.session.commit()
        flash('Cuidador aprovado com sucesso!')
    else:
        flash('Cuidador não encontrado.')
    return redirect(url_for('admin_routes.approve_caregivers'))

@admin_routes.route('/delete_caregiver/<int:caregiver_id>', methods=['POST'])
@login_required
@admin_required
def delete_caregiver(caregiver_id):
    caregiver = Profissional.query.get(caregiver_id)
    if caregiver:
        db.session.delete(caregiver)
        db.session.commit()
        flash('Cuidador excluído com sucesso!')
    else:
        flash('Cuidador não encontrado.')
    return redirect(url_for('admin_routes.approve_caregivers'))

@admin_routes.route('/register_user', methods=['GET', 'POST'])
@login_required
@admin_required
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('admin_routes.register_user'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, role=role)

        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!')
        return redirect(url_for('admin_routes.register_user'))

    return render_template('admin/register_user.html')
