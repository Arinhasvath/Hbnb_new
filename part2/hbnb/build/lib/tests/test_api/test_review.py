"""
Test module for Review API endpoints.
Tests all CRUD operations including DELETE.
"""

import unittest
import json
from app import create_app


class TestReviewAPI(unittest.TestCase):
    """Test case for Review API"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Create test user
        user_data = {
            'email': 'reviewer@test.com',
            'password': 'test123',
            'first_name': 'Test',
            'last_name': 'Reviewer'
        }
        response = self.client.post('/api/v1/user/', json=user_data)
        self.user_id = json.loads(response.data)['id']
        
        # Create test place (needs owner)
        place_data = {
            'title': 'Test Place',
            'description': 'Test Description',
            'price': 100.0,
            'latitude': 43.6,
            'longitude': 3.9,
            'owner_id': self.user_id
        }
        response = self.client.post('/api/v1/place/', json=place_data)
        self.place_id = json.loads(response.data)['id']
        
        self.test_review_data = {
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.user_id,
            'place_id': self.place_id
        }

    def test_create_review(self):
        """Test POST /api/v1/review/"""
        response = self.client.post(
            '/api/v1/review/',
            json=self.test_review_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data['text'], self.test_review_data['text'])
        self.assertEqual(data['rating'], self.test_review_data['rating'])
        self.assertIn('user', data)
        self.assertIn('place', data)

    def test_get_reviews(self):
        """Test GET /api/v1/review/"""
        response = self.client.get('/api/v1/review/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_review(self):
        """Test GET /api/v1/review/<id>"""
        # Create a review first
        create_response = self.client.post(
            '/api/v1/review/',
            json=self.test_review_data
        )
        review_id = json.loads(create_response.data)['id']
        
        response = self.client.get(f'/api/v1/review/{review_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], review_id)
        self.assertIn('user', data)
        self.assertIn('place', data)

    def test_update_review(self):
        """Test PUT /api/v1/review/<id>"""
        # Create a review first
        create_response = self.client.post(
            '/api/v1/review/',
            json=self.test_review_data
        )
        review_id = json.loads(create_response.data)['id']
        
        update_data = {
            'text': 'Updated review text',
            'rating': 4
        }
        response = self.client.put(
            f'/api/v1/review/{review_id}',
            json=update_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['text'], update_data['text'])
        self.assertEqual(data['rating'], update_data['rating'])

    def test_delete_review(self):
        """Test DELETE /api/v1/review/<id>"""
        # Create a review first
        create_response = self.client.post(
            '/api/v1/review/',
            json=self.test_review_data
        )
        review_id = json.loads(create_response.data)['id']
        
        # Test delete
        response = self.client.delete(f'/api/v1/review/{review_id}')
        self.assertEqual(response.status_code, 204)
        
        # Verify review is deleted
        response = self.client.get(f'/api/v1/review/{review_id}')
        self.assertEqual(response.status_code, 404)

    def test_validation(self):
        """Test input validation"""
        # Test invalid rating
        invalid_data = self.test_review_data.copy()
        invalid_data['rating'] = 6
        response = self.client.post('/api/v1/review/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test missing text
        invalid_data = self.test_review_data.copy()
        invalid_data['text'] = ''
        response = self.client.post('/api/v1/review/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test invalid user
        invalid_data = self.test_review_data.copy()
        invalid_data['user_id'] = 'nonexistent'
        response = self.client.post('/api/v1/review/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test invalid place
        invalid_data = self.test_review_data.copy()
        invalid_data['place_id'] = 'nonexistent'
        response = self.client.post('/api/v1/review/', json=invalid_data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
