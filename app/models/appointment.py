from app.db.db import db
from app.models.doctor import Doctor


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="IN_QUEUE")
    diagnose = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")

    def __init__(self, patient_id, doctor_id, datetime, status):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.datetime = datetime
        self.status = status

    @staticmethod
    def is_time_available(doctor_id, appointment_datetime):
        # Check if the datetime is within the doctor's working hours
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return False
        if not (
            doctor.work_start_time
            <= appointment_datetime.time()
            <= doctor.work_end_time
        ):
            return False

        # Check if the doctor is already booked at the given datetime
        conflicting_appointment = Appointment.query.filter_by(
            doctor_id=doctor_id, datetime=appointment_datetime
        ).first()
        return conflicting_appointment is None

    def __repr__(self):
        return f"<Appointment {self.id} with Doctor {self.doctor_id}>"
