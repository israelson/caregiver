import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .config import Config

template_dir = os.path.abspath('../frontend/templates')
static_dir = os.path.abspath('../frontend/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)

db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth_routes.login"

from .models import User
from .routes.admin_routes import admin_routes
from .routes.auth_routes import auth_routes
from .routes.caregiver_routes import caregiver_routes
from .routes.client_routes import client_routes
from .routes.patient_routes import patient_routes
from .routes.record_routes import record_routes

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(caregiver_routes, url_prefix='/caregiver')
app.register_blueprint(client_routes, url_prefix='/client')
app.register_blueprint(patient_routes, url_prefix='/patient')
app.register_blueprint(record_routes, url_prefix='/record')

from .routes.api_routes import api_routes

app.register_blueprint(api_routes)

@app.before_first_request
def create_default_admin():
    if not User.query.filter_by(role='admin').first():
        hashed_password = generate_password_hash('adminpassword', method='sha256')
        default_admin = User(username='admin', password_hash=hashed_password, role='admin')
        db.session.add(default_admin)
        db.session.commit()

@app.route('/')
def index():
    admin_exists = User.query.filter_by(role='admin').first()
    if not admin_exists:
        return redirect(url_for('auth_routes.register_admin'))
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
