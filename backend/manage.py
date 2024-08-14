from flask_migrate import Migrate
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash


migrate = Migrate(app, db)

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print("Database created.")

@app.cli.command('create_user')
def create_user():
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (admin/caregiver): ")
    
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    print(f"User {username} created.")

if __name__ == '__main__':
    app.run(debug=True)
