from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required
from app import db
from app.models import User, Adm

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/register_admin', methods=['GET', 'POST'])
@login_required
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        nome = request.form.get('nome')

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('admin_routes.register_user'))

        # Criptografando a senha
        hashed_password = generate_password_hash(password, method='sha256')

        # Criando um novo usuário na tabela 'user'
        new_user = User(username=username, password_hash=hashed_password, role='admin')
        db.session.add(new_user)
        db.session.commit()

        # Adicionando informações do administrador na tabela 'adm'
        new_adm = Adm(nome=nome, email=email, telefone=telefone)
        db.session.add(new_adm)
        db.session.commit()

        flash('Administrador registrado com sucesso!')
        return redirect(url_for('admin_routes.admin_dashboard'))

    return render_template('admin/register_user.html')

@admin_routes.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_routes.route('/approve_caregivers', methods=['GET', 'POST'])
@login_required
def approve_caregivers():
    # Lógica para aprovação de cuidadores
    return render_template('admin/approve_caregivers.html')
