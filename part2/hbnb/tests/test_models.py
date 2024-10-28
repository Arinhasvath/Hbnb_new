import unittest
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestModels(unittest.TestCase):
    def test_base_model(self):
        base = BaseModel()
        self.assertIsNotNone(base.id)
        self.assertIsNotNone(base.created_at)
        self.assertIsNotNone(base.updated_at)
        
    def test_user_model(self):
        user = User(email="test@example.com", password="password", first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        
    def test_place_model(self):
        place = Place(name="Cozy Apartment", description="A lovely place", number_rooms=2)
        self.assertEqual(place.name, "Cozy Apartment")
        self.assertEqual(place.description, "A lovely place")
        self.assertEqual(place.number_rooms, 2)
        
    def test_review_model(self):
        review = Review(text="Great place!", rating=5)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        
    def test_amenity_model(self):
        amenity = Amenity(name="WiFi")
        self.assertEqual(amenity.name, "WiFi")

if __name__ == '__main__':
    unittest.main()