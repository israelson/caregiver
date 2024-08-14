from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

@auth_routes.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Usuário ou senha incorretos')
        return redirect(url_for('auth_routes.login'))

    login_user(user)
    return redirect(url_for('admin_routes.admin_dashboard') if user.role == 'admin' else url_for('caregiver_routes.caregiver_dashboard'))

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_routes.login'))

@auth_routes.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('auth_routes.register_admin'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, role='admin')

        db.session.add(new_user)
        db.session.commit()
        flash('Administrador registrado com sucesso!')
        return redirect(url_for('auth_routes.login'))

    return render_template('auth/register_admin.html')
