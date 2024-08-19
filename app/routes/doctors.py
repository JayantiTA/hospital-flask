from flask import Blueprint
from flask_login import login_required
from app.controllers.doctors_controller import (
    create_doctor,
    get_doctor,
    get_all_doctors,
    update_doctor,
    delete_doctor,
)


doctors_bp = Blueprint("doctors", __name__)

@doctors_bp.before_request
@login_required
def before_request():
    pass

doctors_bp.route("", methods=["POST"])(create_doctor)
doctors_bp.route("", methods=["GET"])(get_all_doctors)
doctors_bp.route("/<int:doctor_id>", methods=["GET"])(get_doctor)
doctors_bp.route("/<int:doctor_id>", methods=["PUT"])(update_doctor)
doctors_bp.route("/<int:doctor_id>", methods=["DELETE"])(delete_doctor)
