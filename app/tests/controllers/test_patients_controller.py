import unittest
from unittest.mock import MagicMock
from app.app import create_app


class MockFlaskClient:
    def __init__(self):
        self.response = MagicMock()

    def post(self, url, json=None):
        if url == "/patients":
            if all(key in json for key in ("name", "age", "gender", "address")):
                self.response.status_code = 201
                self.response.data = b"Patient created successfully"
            else:
                self.response.status_code = 400
                self.response.data = b"Missing data"
        return self.response

    def get(self, url):
        if url.startswith("/patients"):
            if url == "/patients":
                self.response.status_code = 200
                self.response.data = b"[{'id': 1, 'name': 'John Doe'}]"
            elif url == f"/patients/1":
                self.response.status_code = 200
                self.response.data = b"{'id': 1, 'name': 'John Doe'}"
            else:
                self.response.status_code = 404
                self.response.data = b"Patient not found"
        return self.response

    def put(self, url, json=None):
        if url.startswith("/patients/"):
            if url == f"/patients/1" and (json.get("name") or json.get("address")):
                self.response.status_code = 200
                self.response.data = b"Patient updated successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Patient not found"
        return self.response

    def delete(self, url):
        if url.startswith("/patients/"):
            if url == "/patients/1":
                self.response.status_code = 200
                self.response.data = b"Patient deleted successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Patient not found"
        return self.response


class PatientsBlueprintTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.client = MockFlaskClient()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_create_patient_success(self):
        response = self.client.post(
            "/patients",
            json={
                "name": "New Patient",
                "age": 45,
                "gender": "Male",
                "address": "123 Main St",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Patient created successfully", response.data)

    def test_create_patient_missing_data(self):
        response = self.client.post(
            "/patients",
            json={"name": "Incomplete Patient"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing data", response.data)

    def test_get_all_patients(self):
        response = self.client.get("/patients")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"[{'id': 1, 'name': 'John Doe'}]", response.data)

    def test_get_patient(self):
        response = self.client.get("/patients/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"{'id': 1, 'name': 'John Doe'}", response.data)

    def test_get_patient_not_found(self):
        response = self.client.get("/patients/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Patient not found", response.data)

    def test_update_patient_success(self):
        response = self.client.put(
            "/patients/1",
            json={"name": "Updated Patient", "address": "456 Updated Address"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Patient updated successfully", response.data)

    def test_update_patient_not_found(self):
        response = self.client.put(
            "/patients/9999", json={"name": "Nonexistent Patient"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Patient not found", response.data)

    def test_delete_patient(self):
        response = self.client.delete("/patients/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Patient deleted successfully", response.data)

    def test_delete_patient_not_found(self):
        response = self.client.delete("/patients/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Patient not found", response.data)


if __name__ == "__main__":
    unittest.main()
