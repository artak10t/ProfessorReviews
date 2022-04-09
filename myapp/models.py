from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from myapp import login

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    teacher = db.Column(db.Boolean, default=False)
    moderator = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id}: {self.email}>'

class Professor(UserMixin, db.Model):
    __tablename__ = 'Professor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    department = db.Column(db.String(64))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
