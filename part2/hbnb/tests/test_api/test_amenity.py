"""
Test module for Amenity API endpoints.
Tests all CRUD operations excluding DELETE.
"""

import unittest
import json
from app import create_app


class TestAmenityAPI(unittest.TestCase):
    """Test case for Amenity API"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_amenity_data = {
            'name': 'Wi-Fi'
        }

    def test_create_amenity(self):
        """Test POST /api/v1/amenity/"""
        response = self.client.post(
            '/api/v1/amenity/',
            json=self.test_amenity_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)  # Not 201
        self.assertIn('id', data)
        self.assertEqual(data['name'], self.test_amenity_data['name'])

    def test_get_amenities(self):
        """Test GET /api/v1/amenity/"""
        response = self.client.get('/api/v1/amenity/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_amenity(self):
        """Test GET /api/v1/amenity/<id>"""
        create_response = self.client.post(
            '/api/v1/amenity/',
            json=self.test_amenity_data
        )
        amenity_id = json.loads(create_response.data)['id']
        
        response = self.client.get(f'/api/v1/amenity/{amenity_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], amenity_id)
        self.assertEqual(data['name'], self.test_amenity_data['name'])

    def test_update_amenity(self):
        """Test PUT /api/v1/amenity/<id>"""
        create_response = self.client.post(
            '/api/v1/amenity/',
            json=self.test_amenity_data
        )
        amenity_id = json.loads(create_response.data)['id']
        
        update_data = {
            'name': 'High-Speed Wi-Fi'
        }
        response = self.client.put(
            f'/api/v1/amenity/{amenity_id}',
            json=update_data
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], update_data['name'])

    def test_validation(self):
        """Test input validation"""
        # Empty name
        response = self.client.post(
            '/api/v1/amenity/',
            json={'name': ''}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data),
            {'error': 'Invalid input data'}
        )


if __name__ == '__main__':
    unittest.main()
