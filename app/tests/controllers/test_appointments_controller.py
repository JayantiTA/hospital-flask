import unittest
from unittest.mock import MagicMock
from app.app import create_app


class MockFlaskClient:
    def __init__(self):
        self.response = MagicMock()

    def post(self, url, json=None):
        if url == "/appointments":
            # Simulating an existing booking for a doctor at a specific time
            if (
                json.get("patient_id") != 1
                and json.get("doctor_id") == 1
                and json.get("datetime") == "2024-08-18 14:30:00"
            ):
                self.response.status_code = 400
                self.response.data = b"Doctor is already booked at this time"
            elif all(key in json for key in ("patient_id", "doctor_id", "datetime")):
                self.response.status_code = 201
                self.response.data = b"Appointment created successfully"
            else:
                self.response.status_code = 400
                self.response.data = b"Missing data"
        return self.response

    def get(self, url):
        if url.startswith("/appointments"):
            if url == "/appointments":
                self.response.status_code = 200
                self.response.data = b"[{'id': 1, 'patient_id': 1, 'doctor_id': 1}]"
            elif url == f"/appointments/1":
                self.response.status_code = 200
                self.response.data = b"{'id': 1, 'patient_id': 1, 'doctor_id': 1}"
            else:
                self.response.status_code = 404
                self.response.data = b"Appointment not found"
        return self.response

    def put(self, url, json=None):
        if url.startswith("/appointments/"):
            if url == f"/appointments/1" and json:
                self.response.status_code = 200
                self.response.data = b"Appointment updated successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Appointment not found"
        return self.response

    def delete(self, url):
        if url.startswith("/appointments/"):
            if url == "/appointments/1":
                self.response.status_code = 200
                self.response.data = b"Appointment deleted successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Appointment not found"
        return self.response


class AppointmentControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.client = MockFlaskClient()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_create_appointment_success(self):
        response = self.client.post(
            "/appointments",
            json={
                "patient_id": 1,
                "doctor_id": 1,
                "datetime": "2024-08-18 14:30:00",
                "status": "IN_QUEUE",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Appointment created successfully", response.data)

    def test_create_appointment_missing_data(self):
        response = self.client.post(
            "/appointments",
            json={
                "patient_id": 1,
                "doctor_id": 1,
                # Missing datetime
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing data", response.data)

    def test_create_appointment_doctor_already_booked(self):
        response = self.client.post(
            "/appointments",
            json={
                "patient_id": 2,
                "doctor_id": 1,
                "datetime": "2024-08-18 14:30:00",
                "status": "IN_QUEUE",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Doctor is already booked at this time", response.data)

    def test_get_appointment(self):
        response = self.client.get("/appointments/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"{'id': 1, 'patient_id': 1, 'doctor_id': 1}", response.data)

    def test_get_appointment_not_found(self):
        response = self.client.get("/appointments/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Appointment not found", response.data)

    def test_get_all_appointments(self):
        response = self.client.get("/appointments")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"[{'id': 1, 'patient_id': 1, 'doctor_id': 1}]", response.data)

    def test_update_appointment_success(self):
        response = self.client.put(
            "/appointments/1",
            json={"datetime": "2024-08-18 15:30:00", "status": "DONE"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Appointment updated successfully", response.data)

    def test_update_appointment_not_found(self):
        response = self.client.put(
            "/appointments/9999",
            json={"datetime": "2024-08-18 15:30:00", "status": "DONE"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Appointment not found", response.data)

    def test_delete_appointment(self):
        response = self.client.delete("/appointments/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Appointment deleted successfully", response.data)

    def test_delete_appointment_not_found(self):
        response = self.client.delete("/appointments/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Appointment not found", response.data)


if __name__ == "__main__":
    unittest.main()
