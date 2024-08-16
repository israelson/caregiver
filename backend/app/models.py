from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()



class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    fk_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))
    endereco = db.relationship('Endereco', backref=db.backref('clientes', lazy=True))





class Prontuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=False)
    fk_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    fk_profissional = db.Column(db.Integer, db.ForeignKey('profissional.id'))
    paciente = db.relationship('Paciente', backref=db.backref('prontuarios', lazy=True))
    profissional = db.relationship('Profissional', backref=db.backref('prontuarios', lazy=True))

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    fk_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    fk_profissional = db.Column(db.Integer, db.ForeignKey('profissional.id'))
    paciente = db.relationship('Paciente', backref=db.backref('pedidos', lazy=True))
    profissional = db.relationship('Profissional', backref=db.backref('pedidos', lazy=True))

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_chamado = db.Column(db.DateTime, default=datetime.utcnow)
    fk_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    fk_adm = db.Column(db.Integer, db.ForeignKey('adm.id'))
    pedido = db.relationship('Pedido', backref=db.backref('chamados', lazy=True))
    adm = db.relationship('Adm', backref=db.backref('chamados', lazy=True))

class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)
    fk_profissional = db.Column(db.Integer, db.ForeignKey('profissional.id'))
    fk_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    profissional = db.relationship('Profissional', backref=db.backref('avaliacoes', lazy=True))
    pedido = db.relationship('Pedido', backref=db.backref('avaliacoes', lazy=True))

class Adm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profissional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    especializacoes = db.Column(db.String(255), nullable=False)
    disponibilidade = db.Column(db.String(255), nullable=False)
    certificacoes = db.Column(db.String(255), nullable=False)
    fk_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))
    endereco = db.relationship('Endereco', backref=db.backref('profissionais', lazy=True))
    foto = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='pendente')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'especializacoes': self.especializacoes,
            'disponibilidade': self.disponibilidade,
            'certificacoes': self.certificacoes,
            'fk_endereco': self.fk_endereco,
            'foto': self.foto,
            'status': self.status
        }

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    fk_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    fk_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id'))
    usa_andador = db.Column(db.Boolean, default=False)
    anda = db.Column(db.Boolean, default=False)
    cadeira_de_rodas = db.Column(db.Boolean, default=False)
    alimenta_sozinho = db.Column(db.Boolean, default=False)
    dieta_especial = db.Column(db.String(255), nullable=True)
    banheiro_sozinho = db.Column(db.Boolean, default=False)
    usa_fraldas = db.Column(db.Boolean, default=False)
    medicamentos = db.Column(db.String(255), nullable=True)
    necessidades_especiais = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'fk_cliente': self.fk_cliente,
            'fk_endereco': self.fk_endereco,
            'usa_andador': self.usa_andador,
            'anda': self.anda,
            'cadeira_de_rodas': self.cadeira_de_rodas,
            'alimenta_sozinho': self.alimenta_sozinho,
            'dieta_especial': self.dieta_especial,
            'banheiro_sozinho': self.banheiro_sozinho,
            'usa_fraldas': self.usa_fraldas,
            'medicamentos': self.medicamentos,
            'necessidades_especiais': self.necessidades_especiais
        }
