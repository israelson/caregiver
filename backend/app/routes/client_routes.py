from flask import Blueprint, render_template, redirect, url_for, request
from ..models import Cliente, Paciente, Endereco, db

client_routes = Blueprint('client_routes', __name__)

@client_routes.route('/register')
def client_register():
    return render_template('client/register.html')

@client_routes.route('/register', methods=['POST'])
def create_client():
    data = request.form
    new_client = Cliente(
        nome=data['nome'],
        cpf=data['cpf'],
        email=data['email'],
        telefone=data['telefone'],
        fk_endereco=data['fk_endereco']
    )
    db.session.add(new_client)
    db.session.commit()
    return redirect(url_for('client_routes.client_register'))

@client_routes.route('/register_patient')
def register_patient():
    clients = Cliente.query.all()
    return render_template('client/register_patient.html', clients=clients)

@client_routes.route('/register_patient', methods=['POST'])
def create_patient():
    data = request.form
    new_patient = Paciente(
        nome=data['nome'],
        cpf=data['cpf'],
        email=data['email'],
        telefone=data['telefone'],
        fk_cliente=data['fk_cliente'],
        fk_endereco=data['fk_endereco'],
        usa_andador=data.get('usa_andador', False),
        anda=data.get('anda', False),
        cadeira_de_rodas=data.get('cadeira_de_rodas', False),
        alimenta_sozinho=data.get('alimenta_sozinho', False),
        dieta_especial=data.get('dieta_especial', ''),
        banheiro_sozinho=data.get('banheiro_sozinho', False),
        usa_fraldas=data.get('usa_fraldas', False),
        medicamentos=data.get('medicamentos', ''),
        necessidades_especiais=data.get('necessidades_especiais', '')
    )
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('client_routes.register_patient'))
