import datetime
from email.policy import default
from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from myapp import login

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, index=True)
    password = db.Column(db.String(128))
    teacher = db.Column(db.Boolean, default=False)
    moderator = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id}: {self.email}>'

class Professor(db.Model):
    __tablename__ = 'Professor'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(512))
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(256))
    department = db.Column(db.String(32))
    created = db.Column(db.Date(), default=datetime.datetime.utcnow)
    rating = db.Column(db.Float, default=0)
    difficulty = db.Column(db.Float, default=0)
    reviews = db.Column(db.Integer, default=0)
    awesome = db.Column(db.Float, default=0)
    good = db.Column(db.Float, default=0)
    okay = db.Column(db.Float, default=0)
    bad = db.Column(db.Float, default=0)
    awful = db.Column(db.Float, default=0)

class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True)
    hash_email = db.Column(db.String(512))
    professor_id = db.Column(db.Integer, db.ForeignKey('Professor.id'))
    message = db.Column(db.String(256), default='')
    rating = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    recommend = db.Column(db.Boolean, default=False)
    created = db.Column(db.Date(), default=datetime.datetime.utcnow)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
