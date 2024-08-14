from app import db, app
from app.models import User
from werkzeug.security import generate_password_hash

def create_db():
    with app.app_context():
        db.create_all()
        print("Database created.")

def create_admin_user():
    with app.app_context():
        username = "admin"
        password = "adminpassword"
        role = "admin"
        
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        print(f"Admin user {username} created.")

if __name__ == '__main__':
    create_db()
    create_admin_user()
