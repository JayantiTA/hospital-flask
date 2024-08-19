from flask import request, jsonify
from datetime import datetime
from app.db.db import db
from app.models.doctor import Doctor


def create_doctor():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    gender = data.get('gender')
    birthdate_str = data.get('birthdate')
    work_start_time_str = data.get('work_start_time')
    work_end_time_str = data.get('work_end_time')

    # Validate input
    if not all([name, username, password, gender, birthdate_str, work_start_time_str, work_end_time_str]):
        return jsonify({"error": "Missing data"}), 400

    # Convert and validate data
    try:
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        work_start_time = datetime.strptime(work_start_time_str, '%H:%M:%S').time()
        work_end_time = datetime.strptime(work_end_time_str, '%H:%M:%S').time()
    except ValueError as e:
        return jsonify({"error": f"Invalid date or time format: {e}"}), 400

    # Check if username is already taken
    if Doctor.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_doctor = Doctor(
        name=name,
        username=username,
        password=password,
        gender=gender,
        birthdate=birthdate,
        work_start_time=work_start_time,
        work_end_time=work_end_time
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({"message": "Doctor created successfully"}), 201


def get_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    doctor_data = {
        "id": doctor.id,
        "name": doctor.name,
        "username": doctor.username,
        "gender": doctor.gender,
        "birthdate": doctor.birthdate.isoformat(),
        "work_start_time": doctor.work_start_time.isoformat(),
        "work_end_time": doctor.work_end_time.isoformat()
    }
    return jsonify(doctor_data), 200


def get_all_doctors():
    doctors = Doctor.query.all()
    doctors_data = []
    for doctor in doctors:
        doctor_data = {
            "id": doctor.id,
            "name": doctor.name,
            "username": doctor.username,
            "gender": doctor.gender,
            "birthdate": doctor.birthdate.isoformat(),
            "work_start_time": doctor.work_start_time.isoformat(),
            "work_end_time": doctor.work_end_time.isoformat(),
        }
        doctors_data.append(doctor_data)
    return jsonify(doctors_data), 200


def update_doctor(doctor_id):
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    gender = data.get('gender')
    birthdate_str = data.get('birthdate')
    work_start_time_str = data.get('work_start_time')
    work_end_time_str = data.get('work_end_time')

    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    # Convert and update data
    try:
        if birthdate_str:
            doctor.birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        if work_start_time_str:
            doctor.work_start_time = datetime.strptime(work_start_time_str, '%H:%M:%S').time()
        if work_end_time_str:
            doctor.work_end_time = datetime.strptime(work_end_time_str, '%H:%M:%S').time()
    except ValueError as e:
        return jsonify({"error": f"Invalid date or time format: {e}"}), 400

    if name:
        doctor.name = name
    if username:
        if Doctor.query.filter_by(username=username).first() and doctor.username != username:
            return jsonify({"error": "Username already exists"}), 400
        doctor.username = username
    if password:
        doctor.password = password
    if gender:
        doctor.gender = gender

    db.session.commit()
    return jsonify({"message": "Doctor updated successfully"}), 200


def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"message": "Doctor deleted successfully"}), 200
