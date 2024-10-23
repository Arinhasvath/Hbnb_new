"""
Test module for Place API endpoints.
Tests all CRUD operations excluding DELETE.
"""

import unittest
import json
from app import create_app


class TestPlaceAPI(unittest.TestCase):
    """Test case for Place API"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Create a test user first
        user_data = {
            'email': 'owner@test.com',
            'password': 'test123',
            'first_name': 'Test',
            'last_name': 'Owner'
        }
        response = self.client.post('/api/v1/user/', json=user_data)
        self.owner_id = json.loads(response.data)['id']
        
        # Create test amenity
        amenity_data = {'name': 'WiFi'}
        response = self.client.post('/api/v1/amenity/', json=amenity_data)
        self.amenity_id = json.loads(response.data)['id']
        
        self.test_place_data = {
            'title': 'Test Place',
            'description': 'Test Description',
            'price': 100.0,
            'latitude': 43.6,
            'longitude': 3.9,
            'owner_id': self.owner_id,
            'amenity_ids': [self.amenity_id]
        }

    def test_create_place(self):
        """Test POST /api/v1/place/"""
        response = self.client.post(
            '/api/v1/place/',
            json=self.test_place_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data['title'], self.test_place_data['title'])
        self.assertIn('owner', data)
        self.assertIn('amenities', data)

    def test_get_places(self):
        """Test GET /api/v1/place/"""
        response = self.client.get('/api/v1/place/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_place(self):
        """Test GET /api/v1/place/<id>"""
        # Create a place first
        create_response = self.client.post(
            '/api/v1/place/',
            json=self.test_place_data
        )
        place_id = json.loads(create_response.data)['id']
        
        response = self.client.get(f'/api/v1/place/{place_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], place_id)
        self.assertIn('owner', data)
        self.assertIn('amenities', data)

    def test_update_place(self):
        """Test PUT /api/v1/place/<id>"""
        # Create a place first
        create_response = self.client.post(
            '/api/v1/place/',
            json=self.test_place_data
        )
        place_id = json.loads(create_response.data)['id']
        
        update_data = {
            'title': 'Updated Place',
            'price': 150.0
        }
        response = self.client.put(
            f'/api/v1/place/{place_id}',
            json=update_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], update_data['title'])
        self.assertEqual(float(data['price']), update_data['price'])

    def test_validation(self):
        """Test input validation"""
        # Test invalid price
        invalid_data = self.test_place_data.copy()
        invalid_data['price'] = -100
        response = self.client.post('/api/v1/place/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test invalid coordinates
        invalid_data = self.test_place_data.copy()
        invalid_data['latitude'] = 91
        response = self.client.post('/api/v1/place/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test invalid owner
        invalid_data = self.test_place_data.copy()
        invalid_data['owner_id'] = 'nonexistent'
        response = self.client.post('/api/v1/place/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_relations(self):
        """Test place relations"""
        # Create place
        response = self.client.post(
            '/api/v1/place/',
            json=self.test_place_data
        )
        data = json.loads(response.data)
        
        # Check owner details
        self.assertIn('owner', data)
        self.assertEqual(data['owner']['id'], self.owner_id)
        
        # Check amenities
        self.assertIn('amenities', data)
        self.assertEqual(len(data['amenities']), 1)
        self.assertEqual(data['amenities'][0]['id'], self.amenity_id)


if __name__ == '__main__':
    unittest.main()
