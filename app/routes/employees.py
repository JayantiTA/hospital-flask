from flask import Blueprint
from flask_login import login_required
from app.controllers.employees_controller import (
    create_employee,
    get_employee,
    get_all_employees,
    update_employee,
    delete_employee,
)


employees_bp = Blueprint("employees", __name__)

@employees_bp.before_request
@login_required
def before_request():
    pass

employees_bp.route("", methods=["POST"])(create_employee)
employees_bp.route("", methods=["GET"])(get_all_employees)
employees_bp.route("/<int:employee_id>", methods=["GET"])(get_employee)
employees_bp.route("/<int:employee_id>", methods=["PUT"])(update_employee)
employees_bp.route("/<int:employee_id>", methods=["DELETE"])(delete_employee)
