from flask import Flask
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.modules.main.route import main_bp
from app.db.db import db
from app.controllers.patients_controller import update_patients_from_bigquery
from app.routes.patients import patients_bp
from app.routes.doctors import doctors_bp
from app.routes.employees import employees_bp
from app.routes.appointments import appointments_bp
from app.routes.auth import auth_bp


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(appointments_bp, url_prefix="/appointments")
        app.register_blueprint(patients_bp, url_prefix="/patients")
        app.register_blueprint(doctors_bp, url_prefix="/doctors")
        app.register_blueprint(employees_bp, url_prefix="/employees")


def initialize_db(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()


def initialize_auth(app: Flask):
    with app.app_context():
        login_manager = LoginManager()
        login_manager.init_app(app)


def start_scheduler(app):
    with app.app_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=update_patients_from_bigquery, trigger="interval", hours=24
        )
        scheduler.start()

        # Shut down the scheduler when exiting the app
        atexit.register(scheduler.shutdown)
