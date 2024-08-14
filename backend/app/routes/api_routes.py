from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from app import db
from app.models import User, Profissional, Paciente

api_routes = Blueprint('api_routes', __name__)

# Routes for Users
@api_routes.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_routes.route('/api/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@api_routes.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@api_routes.route('/api/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='sha256')
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify(user.to_dict())

@api_routes.route('/api/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Routes for Caregivers
@api_routes.route('/api/caregivers', methods=['GET'])
def get_caregivers():
    caregivers = Profissional.query.all()
    return jsonify([caregiver.to_dict() for caregiver in caregivers])

@api_routes.route('/api/caregiver/<int:id>', methods=['GET'])
def get_caregiver(id):
    caregiver = Profissional.query.get_or_404(id)
    return jsonify(caregiver.to_dict())

@api_routes.route('/api/caregivers', methods=['POST'])
def create_caregiver():
    data = request.get_json()
    new_caregiver = Profissional(
        nome=data['nome'],
        cpf=data['cpf'],
        email=data['email'],
        telefone=data['telefone'],
        especializacoes=data['especializacoes'],
        disponibilidade=data['disponibilidade'],
        certificacoes=data['certificacoes'],
        fk_endereco=data['fk_endereco'],
        status='pendente'
    )
    db.session.add(new_caregiver)
    db.session.commit()
    return jsonify(new_caregiver.to_dict()), 201

@api_routes.route('/api/caregiver/<int:id>', methods=['PUT'])
def update_caregiver(id):
    caregiver = Profissional.query.get_or_404(id)
    data = request.get_json()
    caregiver.nome = data.get('nome', caregiver.nome)
    caregiver.cpf = data.get('cpf', caregiver.cpf)
    caregiver.email = data.get('email', caregiver.email)
    caregiver.telefone = data.get('telefone', caregiver.telefone)
    caregiver.especializacoes = data.get('especializacoes', caregiver.especializacoes)
    caregiver.disponibilidade = data.get('disponibilidade', caregiver.disponibilidade)
    caregiver.certificacoes = data.get('certificacoes', caregiver.certificacoes)
    caregiver.fk_endereco = data.get('fk_endereco', caregiver.fk_endereco)
    caregiver.status = data.get('status', caregiver.status)
    db.session.commit()
    return jsonify(caregiver.to_dict())

@api_routes.route('/api/caregiver/<int:id>', methods=['DELETE'])
def delete_caregiver(id):
    caregiver = Profissional.query.get_or_404(id)
    db.session.delete(caregiver)
    db.session.commit()
    return '', 204

# Routes for Patients
@api_routes.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Paciente.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@api_routes.route('/api/patient/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Paciente.query.get_or_404(id)
    return jsonify(patient.to_dict())

@api_routes.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    new_patient = Paciente(
        nome=data['nome'],
        cpf=data['cpf'],
        email=data['email'],
        telefone=data['telefone'],
        fk_cliente=data['fk_cliente'],
        fk_endereco=data['fk_endereco'],
        usa_andador=data['usa_andador'],
        anda=data['anda'],
        cadeira_de_rodas=data['cadeira_de_rodas'],
        alimenta_sozinho=data['alimenta_sozinho'],
        dieta_especial=data['dieta_especial'],
        banheiro_sozinho=data['banheiro_sozinho'],
        usa_fraldas=data['usa_fraldas'],
        medicamentos=data['medicamentos'],
        necessidades_especiais=data['necessidades_especiais']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(new_patient.to_dict()), 201

@api_routes.route('/api/patient/<int:id>', methods=['PUT'])
def update_patient(id):
    patient = Paciente.query.get_or_404(id)
    data = request.get_json()
    patient.nome = data.get('nome', patient.nome)
    patient.cpf = data.get('cpf', patient.cpf)
    patient.email = data.get('email', patient.email)
    patient.telefone = data.get('telefone', patient.telefone)
    patient.fk_cliente = data.get('fk_cliente', patient.fk_cliente)
    patient.fk_endereco = data.get('fk_endereco', patient.fk_endereco)
    patient.usa_andador = data.get('usa_andador', patient.usa_andador)
    patient.anda = data.get('anda', patient.anda)
    patient.cadeira_de_rodas = data.get('cadeira_de_rodas', patient.cadeira_de_rodas)
    patient.alimenta_sozinho = data.get('alimenta_sozinho', patient.alimenta_sozinho)
    patient.dieta_especial = data.get('dieta_especial', patient.dieta_especial)
    patient.banheiro_sozinho = data.get('banheiro_sozinho', patient.banheiro_sozinho)
    patient.usa_fraldas = data.get('usa_fraldas', patient.usa_fraldas)
    patient.medicamentos = data.get('medicamentos', patient.medicamentos)
    patient.necessidades_especiais = data.get('necessidades_especiais', patient.necessidades_especiais)
    db.session.commit()
    return jsonify(patient.to_dict())

@api_routes.route('/api/patient/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Paciente.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return '', 204
