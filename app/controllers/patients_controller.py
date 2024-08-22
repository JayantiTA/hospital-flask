from flask import request, jsonify
from google.cloud import bigquery
from app.db.db import db
from app.models.patient import Patient
from datetime import datetime


def create_patient():
    data = request.get_json()
    name = data.get("name")
    gender = data.get("gender")
    birthdate_str = data.get("birthdate")
    no_ktp = data.get("no_ktp")
    address = data.get("address")

    if not all([name, gender, birthdate_str, no_ktp, address]):
        return jsonify({"error": "Missing data"}), 400

    if len(no_ktp) != 16 or no_ktp.isdigit() is False:
        return jsonify({"error": "Invalid no KTP"}), 400

    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    if Patient.query.filter_by(no_ktp=no_ktp).first():
        return jsonify({"error": "Patient with this KTP already exists"}), 400

    new_patient = Patient(
        name=name,
        gender=gender,
        birthdate=birthdate,
        no_ktp=no_ktp,
        address=address,
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient created successfully"}), 201


def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient_data = {
        "id": patient.id,
        "name": patient.name,
        "gender": patient.gender,
        "birthdate": patient.birthdate.isoformat(),
        "no_ktp": patient.no_ktp,
        "address": patient.address,
        "vaccine_type": patient.vaccine_type,
        "vaccine_count": patient.vaccine_count,
    }
    return jsonify(patient_data), 200


def get_all_patients():
    patients = Patient.query.all()
    patients_data = [
        {
             "id": patient.id,
            "name": patient.name,
            "gender": patient.gender,
            "birthdate": patient.birthdate.isoformat(),
            "no_ktp": patient.no_ktp,
            "address": patient.address,
            "vaccine_type": patient.vaccine_type,
            "vaccine_count": patient.vaccine_count,
        }
        for patient in patients
    ]
    return jsonify(patients_data), 200


def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    name = data.get("name")
    gender = data.get("gender")
    birthdate_str = data.get("birthdate")
    no_ktp = data.get("no_ktp")
    address = data.get("address")

    if birthdate_str:
        try:
            patient.birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    if name:
        patient.name = name
    if gender:
        patient.gender = gender
    if no_ktp:
        if Patient.query.filter_by(no_ktp=no_ktp).first() and patient.no_ktp != no_ktp:
            return jsonify({"error": "Patient with this KTP already exists"}), 400
        patient.no_ktp = no_ktp
    if address:
        patient.address = address

    db.session.commit()
    return jsonify({"message": "Patient updated successfully"}), 200


def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"}), 200


def update_patients_from_bigquery():
    client = bigquery.Client()

    query = """
    SELECT no_ktp, vaccine_type, COUNT(vaccine_type) as vaccine_count
    FROM `delman-internal.delman_interview.vaccine_data`
    GROUP BY no_ktp, vaccine_type
    """
    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        patient = Patient.query.filter_by(no_ktp=row.no_ktp).with_for_update().first()
        if patient:
            patient.name = row.full_name
            patient.birthdate = row.birthdate
            patient.vaccine_status = row.vaccine_status
            patient.vaccine_count = row.vaccine_count
            db.session.commit()
        else:
            new_patient = Patient(
                no_ktp=row.no_ktp,
                name=row.full_name,
                birthdate=row.birthdate,
                vaccine_status=row.vaccine_status,
                vaccine_count=row.vaccine_count,
            )
            db.session.add(new_patient)
            db.session.commit()

    print("Patients data updated successfully from BigQuery.")
