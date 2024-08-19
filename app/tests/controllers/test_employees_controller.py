import unittest
from unittest.mock import MagicMock
from app.app import create_app


class MockFlaskClient:
    def __init__(self):
        self.response = MagicMock()

    def post(self, url, json=None):
        # Mock response for POST requests
        if url == "/login":
            if (
                json.get("username") == "testuser"
                and json.get("password") == "testpassword"
            ):
                self.response.status_code = 200
                self.response.data = b"Login successfully"
            else:
                self.response.status_code = 401
                self.response.data = b"Invalid credential"
        elif url == "/create_employee":
            if all(
                key in json
                for key in ("name", "username", "password", "gender", "birthdate")
            ):
                self.response.status_code = 201
                self.response.data = b"Employee created successfully"
            else:
                self.response.status_code = 400
                self.response.data = b"Missing data"
        elif url == "/logout":
            self.response.status_code = 200
            self.response.data = b"Logged out successfully"
        # Add more conditions as needed
        return self.response

    def get(self, url):
        # Mock response for GET requests
        if url.startswith("/employee/"):
            if url == f"/employee/1":
                self.response.status_code = 200
                self.response.data = b"testuser"
            else:
                self.response.status_code = 404
                self.response.data = b"Employee not found"
        return self.response

    def put(self, url, json=None):
        # Mock response for PUT requests
        if url.startswith("/employee/"):
            if url == f"/employee/1" and (json.get("name") or json.get("username")):
                self.response.status_code = 200
                self.response.data = b"Employee updated successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Employee not found"
        return self.response

    def delete(self, url):
        # Mock response for DELETE requests
        if url.startswith("/employee/"):
            if url == "/employee/1":
                self.response.status_code = 200
                self.response.data = b"Employee deleted successfully"
            else:
                self.response.status_code = 404
                self.response.data = b"Employee not found"
        return self.response


class EmployeeControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.client = MockFlaskClient()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_login_success(self):
        response = self.client.post(
            "/login", json={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successfully", response.data)

    def test_login_failure(self):
        response = self.client.post(
            "/login", json={"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid credential", response.data)

    def test_logout(self):
        response = self.client.post("/logout")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logged out successfully", response.data)

    def test_create_employee_success(self):
        response = self.client.post(
            "/create_employee",
            json={
                "name": "New Employee",
                "username": "newuser",
                "password": "newpassword",
                "gender": "Female",
                "birthdate": "1995-05-15",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Employee created successfully", response.data)

    def test_create_employee_missing_data(self):
        response = self.client.post(
            "/create_employee",
            json={
                "name": "Incomplete Employee",
                "username": "incompleteuser",
                "password": "incompletepassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing data", response.data)

    def test_get_employee(self):
        response = self.client.get("/employee/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testuser", response.data)

    def test_get_employee_not_found(self):
        response = self.client.get("/employee/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Employee not found", response.data)

    def test_update_employee_success(self):
        response = self.client.put(
            "/employee/1",
            json={
                "name": "Updated Name",
                "username": "updateduser",
                "birthdate": "1990-01-01",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Employee updated successfully", response.data)

    def test_update_employee_not_found(self):
        response = self.client.put(
            "/employee/9999", json={"name": "Nonexistent Employee"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Employee not found", response.data)

    def test_delete_employee(self):
        response = self.client.delete("/employee/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Employee deleted successfully", response.data)

    def test_delete_employee_not_found(self):
        response = self.client.delete("/employee/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Employee not found", response.data)


if __name__ == "__main__":
    unittest.main()
