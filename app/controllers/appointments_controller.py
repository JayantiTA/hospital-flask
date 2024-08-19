from flask import request, jsonify
from app.db.db import db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from datetime import datetime


VALID_STATUSES = ["IN_QUEUE", "DONE", "CANCELLED"]


def create_appointment():
    data = request.get_json()
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    datetime_str = data.get("datetime")
    status = data.get("status")

    if not all([patient_id, doctor_id, datetime_str]):
        return jsonify({"error": "Missing data"}), 400

    try:
        appointment_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

    appointment_time = appointment_datetime.time()

    # Validate status as a string
    if status and status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status value"}), 400

    # Check if patient exists
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Check if doctor exists
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    # Check for overlapping appointments (ignoring seconds)
    overlapping_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        db.extract("hour", Appointment.datetime) == appointment_datetime.hour,
        db.extract("minute", Appointment.datetime) == appointment_datetime.minute,
    ).all()

    if overlapping_appointments:
        return jsonify({"error": "Doctor is already booked at this time"}), 400

    # Check if the appointment time is within doctor's working hours
    if not (doctor.work_start_time <= appointment_time <= doctor.work_end_time):
        return (
            jsonify({"error": "Appointment time is outside of doctor's working hours"}),
            400,
        )

    # Create new appointment
    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        datetime=appointment_datetime,
        status=status,
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created successfully"}), 201


def get_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment_data = {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "datetime": appointment.datetime.isoformat(),
        "status": appointment.status,
        "diagnose": appointment.diagnose,
        "notes": appointment.notes,
    }
    return jsonify(appointment_data), 200


def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify(appointments), 200


def update_appointment(appointment_id):
    data = request.get_json()
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    datetime_str = data.get("datetime")
    status = data.get("status")
    diagnose = data.get("diagnose")
    notes = data.get("notes")

    if datetime_str:
        try:
            new_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            # Check if new datetime overlaps with other appointments for the same doctor
            if Appointment.query.filter(
                Appointment.doctor_id == doctor_id,
                Appointment.id != appointment_id,
                db.extract("hour", Appointment.datetime) == new_datetime.hour,
                db.extract("minute", Appointment.datetime) == new_datetime.minute,
            ).first():
                return jsonify({"error": "Doctor is already booked at this time"}), 400

            # Check if new datetime is within doctor's working hours
            doctor = Doctor.query.get(doctor_id)
            if not (
                doctor.work_start_time <= new_datetime.time() <= doctor.work_end_time
            ):
                return (
                    jsonify(
                        {
                            "error": "Appointment time is outside of doctor's working hours"
                        }
                    ),
                    400,
                )

            appointment.datetime = new_datetime
        except ValueError:
            return jsonify({"error": "Invalid datetime format"}), 400

    if status:
        if status not in VALID_STATUSES:
            return jsonify({"error": "Invalid status value"}), 400
        appointment.status = status
    if diagnose:
        appointment.diagnose = diagnose
    if notes:
        appointment.notes = notes

    db.session.commit()
    return jsonify({"message": "Appointment updated successfully"}), 200


def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"}), 200
