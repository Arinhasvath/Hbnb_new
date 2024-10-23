"""
Test module for User API endpoints.
Tests all CRUD operations excluding DELETE.
"""
import os
import sys
import unittest
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models.user import User


class TestUserAPI(unittest.TestCase):
    """Test case for User API"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_user_data = {
            'email': 'test@test.com',
            'password': 'test123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user(self):
        """Test POST /api/v1/user/"""
        # Test valid user creation
        response = self.client.post(
            '/api/v1/user/',
            json=self.test_user_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data['email'], self.test_user_data['email'])
        self.assertNotIn('password', data)  # Password should not be in response
        
        # Test invalid data
        invalid_data = self.test_user_data.copy()
        invalid_data['email'] = 'invalid'
        response = self.client.post('/api/v1/user/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        """Test GET /api/v1/user/"""
        response = self.client.get('/api/v1/user/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_user(self):
        """Test GET /api/v1/user/<id>"""
        # First create a user
        create_response = self.client.post(
            '/api/v1/user/',
            json=self.test_user_data
        )
        user_id = json.loads(create_response.data)['id']
        
        # Test get existing user
        response = self.client.get(f'/api/v1/user/{user_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], user_id)
        self.assertNotIn('password', data)
        
        # Test get non-existent user
        response = self.client.get('/api/v1/user/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test PUT /api/v1/user/<id>"""
        # First create a user
        create_response = self.client.post(
            '/api/v1/user/',
            json=self.test_user_data
        )
        user_id = json.loads(create_response.data)['id']
        
        # Test valid update
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.put(
            f'/api/v1/user/{user_id}',
            json=update_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['first_name'], update_data['first_name'])
        
        # Test invalid update
        response = self.client.put(
            f'/api/v1/user/{user_id}',
            json={'email': 'invalid'}
        )
        self.assertEqual(response.status_code, 400)

    def test_validation(self):
        """Test input validation"""
        # Test missing required fields
        response = self.client.post('/api/v1/user/', json={})
        self.assertEqual(response.status_code, 400)
        
        # Test invalid email
        invalid_data = self.test_user_data.copy()
        invalid_data['email'] = 'notanemail'
        response = self.client.post('/api/v1/user/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test short password
        invalid_data = self.test_user_data.copy()
        invalid_data['password'] = '12345'
        response = self.client.post('/api/v1/user/', json=invalid_data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
