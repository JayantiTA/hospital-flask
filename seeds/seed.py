import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from wsgi import app
from app.db.db import db
from app.models.employee import Employee
from datetime import date


def seed_database():
    with app.app_context():
        if Employee.query.first():
            print("Database already seeded.")
            return

        employee = Employee(
            name="John Doe",
            username="johndoe",
            password="securepassword123",
            gender="Male",
            birthdate=date(1990, 1, 1),
        )

        try:
            db.session.add(employee)
            db.session.commit()
            print("Database seeded with initial data.")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_database()
