from flask import Blueprint
from app.controllers.employees_controller import login, logout


auth_bp = Blueprint("auth", __name__)

auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/logout", methods=["POST"])(logout)
