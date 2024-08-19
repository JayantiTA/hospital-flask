from flask import request, jsonify
from flask_login import login_user, logout_user
from datetime import datetime
from app.db.db import db
from app.models.employee import Employee


def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    employee = Employee.query.filter_by(username=username).first()

    if employee and employee.check_password(password):
        login_user(employee)
        return jsonify({"message": "Login successfully"}), 200
    else:
        return jsonify({"error": "Invalid credential"}), 401


def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


def create_employee():
    data = request.get_json()
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    gender = data.get("gender")
    birthdate_str = data.get("birthdate")

    # Validate input
    if not all([name, username, password, gender, birthdate_str]):
        return jsonify({"error": "Missing data"}), 400

    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    except ValueError as e:
        return jsonify({"error": f"Invalid date or time format: {e}"}), 400

    # Check if username is already taken
    if Employee.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Create and save the new employee
    new_employee = Employee(
        name=name,
        username=username,
        password=password,
        gender=gender,
        birthdate=birthdate,
    )
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee created successfully"}), 201


def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    employee_data = {
        "id": employee.id,
        "name": employee.name,
        "username": employee.username,
        "gender": employee.gender,
        "birthdate": employee.birthdate.isoformat(),
    }
    return jsonify(employee_data), 200


def get_all_employees():
    employees = Employee.query.all()
    employees_data = []
    for employee in employees:
        employee_data = {
            "id": employee.id,
            "name": employee.name,
            "username": employee.username,
            "gender": employee.gender,
            "birthdate": employee.birthdate.isoformat(),
        }
        employees_data.append(employee_data)
    return jsonify(employees_data), 200


def update_employee(employee_id):
    data = request.get_json()
    name = data.get("name")
    username = data.get("username")
    password_default = data.get("password")
    gender = data.get("gender")
    birthdate_str = data.get("birthdate")

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    try:
        if birthdate_str:
            employee.birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    except ValueError as e:
        return jsonify({"error": f"Invalid date or time format: {e}"}), 400

    if name:
        employee.name = name
    if username:
        employee = Employee.query.filter_by(username=username).first()
        if employee and employee.id != employee_id:
            return jsonify({"error": "Username already exists"}), 400
        employee.username = username
    if password_default:
        employee.password = password_default
    if gender:
        employee.gender = gender

    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200


def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200
