import unittest
from unittest.mock import MagicMock
from app.app import create_app


class MockFlaskClient:
    def __init__(self):
        self.response = MagicMock()

    def post(self, url, json=None):
        if url == "/create_doctor":
            if all(
                key in json
                for key in (
                    "name",
                    "username",
                    "password",
                    "gender",
                    "birthdate",
                    "work_start_time",
                    "work_end_time",
                )
            ):
                self.response.status_code = 201
                self.response.data = b"Doctor created successfully"
            else:
                self.response.status_code = 400
                self.response.data = b"Missing data"
        # More POST requests can be mocked similarly
        return self.response

    def get(self, url):
        if url.startswith("/doctor/"):
            if url == f"/doctor/1":
                self.response.status_code = 200
                self.response.data = b"Doctor found"
            else:
                self.response.status_code = 404
                self.response.data = b"Doctor not found"
        return self.response

    def put(self, url, json=None):
        if url.startswith("/doctor/"):
            if url == f"/doctor/1" and (json.get("name") or json.get("username")):
                self.response.status_code = 200
                self.response.data = b"Doctor updated successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Doctor not found"
        return self.response

    def delete(self, url):
        if url.startswith("/doctor/"):
            if url == "/doctor/1":
                self.response.status_code = 200
                self.response.data = b"Doctor deleted successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Doctor not found"
        return self.response


class DoctorControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.client = MockFlaskClient()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_create_doctor_success(self):
        response = self.client.post(
            "/create_doctor",
            json={
                "name": "New Doctor",
                "username": "newdoctor",
                "password": "newpassword",
                "gender": "Female",
                "birthdate": "1980-05-15",
                "work_start_time": "09:00:00",
                "work_end_time": "17:00:00",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Doctor created successfully", response.data)

    def test_create_doctor_missing_data(self):
        response = self.client.post(
            "/create_doctor",
            json={
                "name": "Incomplete Doctor",
                "username": "incompletedoctor",
                "password": "incompletepassword",
                # Missing other required fields
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing data", response.data)

    def test_get_doctor(self):
        response = self.client.get("/doctor/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Doctor found", response.data)

    def test_get_doctor_not_found(self):
        response = self.client.get("/doctor/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Doctor not found", response.data)

    def test_update_doctor_success(self):
        response = self.client.put(
            "/doctor/1",
            json={
                "name": "Updated Doctor",
                "username": "updateddoctor",
                "birthdate": "1980-01-01",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Doctor updated successfully", response.data)

    def test_update_doctor_not_found(self):
        response = self.client.put("/doctor/9999", json={"name": "Nonexistent Doctor"})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Doctor not found", response.data)

    def test_delete_doctor(self):
        response = self.client.delete("/doctor/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Doctor deleted successfully", response.data)

    def test_delete_doctor_not_found(self):
        response = self.client.delete("/doctor/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Doctor not found", response.data)


if __name__ == "__main__":
    unittest.main()
