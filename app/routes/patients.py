from flask import Blueprint
from flask_login import login_required
from app.controllers.patients_controller import (
    create_patient,
    get_patient,
    get_all_patients,
    update_patient,
    delete_patient,
)


patients_bp = Blueprint("patients", __name__)

@patients_bp.before_request
@login_required
def before_request():
    pass

patients_bp.route("", methods=["POST"])(create_patient)
patients_bp.route("", methods=["GET"])(get_all_patients)
patients_bp.route("/<int:patient_id>", methods=["GET"])(get_patient)
patients_bp.route("/<int:patient_id>", methods=["PUT"])(update_patient)
patients_bp.route("/<int:patient_id>", methods=["DELETE"])(delete_patient)
