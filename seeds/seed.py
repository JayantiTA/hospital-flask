from wsgi import app, db
from app.models import Employee


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
            birthdate="1990-01-01",
        )

        db.session.add(employee)
        db.session.commit()
        print("Database seeded with initial data.")


if __name__ == "__main__":
    seed_database()
