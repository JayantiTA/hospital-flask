from app.db.db import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    no_ktp = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    vaccine_type = db.Column(db.String(100), nullable=True)
    vaccine_count = db.Column(db.Integer, nullable=True)

    # appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __init__(self, name, gender, birthdate, no_ktp, address):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.no_ktp = no_ktp
        self.address = address

    def __repr__(self):
        return f"<Patient {self.no_ktp}>"
