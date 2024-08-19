from flask import Blueprint
from flask_login import login_required
from app.controllers.appointments_controller import (
    create_appointment,
    get_appointment,
    get_all_appointments,
    update_appointment,
    delete_appointment,
)


appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.before_request
@login_required
def before_request():
    pass

appointments_bp.route("", methods=["POST"])(create_appointment)
appointments_bp.route("", methods=["GET"])(get_all_appointments)
appointments_bp.route("/<int:appointment_id>", methods=["GET"])(
    get_appointment
)
appointments_bp.route("/<int:appointment_id>", methods=["PUT"])(
    update_appointment
)
appointments_bp.route("/<int:appointment_id>", methods=["DELETE"])(
    delete_appointment
)
