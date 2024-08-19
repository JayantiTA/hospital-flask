from app.db.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column('password', db.String(128), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    work_start_time = db.Column(db.Time, nullable=False)
    work_end_time = db.Column(db.Time, nullable=False)

    # appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __init__(
        self,
        name,
        username,
        password,
        gender,
        birthdate,
        work_start_time,
        work_end_time,
    ):
        self.name = name
        self.username = username
        self.password = password
        self.gender = gender
        self.birthdate = birthdate
        self.work_start_time = work_start_time
        self.work_end_time = work_end_time

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"<Doctor {self.username}>"
