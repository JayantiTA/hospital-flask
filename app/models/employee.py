from app.db.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column("password", db.String(128), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    def __init__(self, name, username, password, gender, birthdate):
        self.name = name
        self.username = username
        self.password = password
        self.gender = gender
        self.birthdate = birthdate

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"<Employee {self.username}>"
