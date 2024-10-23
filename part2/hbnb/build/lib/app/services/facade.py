"""
HBnB Facade Service
"""

class HBnBFacade:
    """Facade for managing business operations"""
    
    def __init__(self):
        """Initialize storage"""
        self.users = {}
        self.places = {}
        self.reviews = {}
        self.amenities = {}

    # User operations
    def create_user(self, data):
        from app.models.user import User
        user = User(**data)
        user.validate()
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_all_users(self):
        return list(self.users.values())

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if user:
            user.update(data)
        return user

    # Place operations
    def create_place(self, data):
        from app.models.place import Place
        place = Place(**data)
        if owner := self.get_user(place.owner_id):
            place.owner = owner
        place.validate()
        self.places[place.id] = place
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def get_all_places(self):
        return list(self.places.values())

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if place:
            place.update(data)
        return place

    # Review operations
    def create_review(self, data):
        from app.models.review import Review
        review = Review(**data)
        if user := self.get_user(review.user_id):
            review.user = user
        if place := self.get_place(review.place_id):
            review.place = place
        review.validate()
        self.reviews[review.id] = review
        return review

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        return list(self.reviews.values())

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if review:
            review.update(data)
        return review

    def delete_review(self, review_id):
        if review_id in self.reviews:
            del self.reviews[review_id]
            return True
        return False

    # Amenity operations
    def create_amenity(self, data):
        from app.models.amenity import Amenity
        amenity = Amenity(**data)
        amenity.validate()
        self.amenities[amenity.id] = amenity
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def get_all_amenities(self):
        return list(self.amenities.values())

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(data)
        return amenity