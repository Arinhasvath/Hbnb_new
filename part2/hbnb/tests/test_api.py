import unittest
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_users(self):
        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post('/api/v1/users', json=user_data)
        self.assertEqual(response.status_code, 201)

    # Ajoutez d'autres tests pour les autres endpoints

if __name__ == '__main__':
    unittest.main()