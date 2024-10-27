from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize repositories here
            cls._instance.user_repo = InMemoryRepository(User)
            cls._instance.amenity_repo = InMemoryRepository(Amenity)
            cls._instance.place_repo = InMemoryRepository(Place)
            cls._instance.review_repo = InMemoryRepository(Review)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

# Users methods
    def get_user(self, user_id: str):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def create_user(self, user_data: dict):
        """Create new user"""
        if not user_data:
            raise ValueError("User data cannot be empty")
        if 'email' not in user_data:
            raise ValueError("Email is required")

        all_users = self.get_all_users()
        if any(user.email == user_data['email'] for user in all_users):
            raise ValueError("Email already registered")

        try:
            user = User(**user_data)
            self.user_repo.add(user)
            return user
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def update_user(self, user_id: str, user_data: dict):
        """Update existing user"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if 'email' in user_data:
            all_users = self.get_all_users()
            if any(u.email == user_data['email'] and u.id != user_id for u in all_users):
                raise ValueError("Email already registered")

        try:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.validate()
            self.user_repo.update(user_id, user)
            return user
        except Exception as e:
            raise ValueError(f"Error updating user: {str(e)}")

# Amenity methods
    def get_amenity(self, amenity_id: str):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def create_amenity(self, amenity_data: dict):
        """Create new amenity"""
        if not amenity_data:
            raise ValueError("Amenity data cannot be empty")
        if 'name' not in amenity_data:
            raise ValueError("Name is required")

        try:
            amenity = Amenity(**amenity_data)
            self.amenity_repo.add(amenity)
            return amenity
        except Exception as e:
            raise ValueError(f"Error creating amenity: {str(e)}")

    def update_amenity(self, amenity_id: str, amenity_data: dict):
        """Update existing amenity"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        try:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
            amenity.validate()
            self.amenity_repo.update(amenity_id, amenity)
            return amenity
        except Exception as e:
            raise ValueError(f"Error updating amenity: {str(e)}")
        
# Place methods
    def create_place(self, place_data):
        """Create new place"""
        try:
            if not place_data:
                raise ValueError("Place data cannot be empty")
            
            # Validate required fields
            required_fields = ['title', 'description', 'price', 'latitude',
                            'longitude', 'owner_id']
            for field in required_fields:
                if field not in place_data:
                    raise ValueError(f"{field} is required")

            # Validate owner exists
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError(f"Owner with id {place_data['owner_id']} not found")

            # Validate amenities if provided
            if 'amenity_ids' in place_data:
                valid_amenities = []
                for amenity_id in place_data['amenity_ids']:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity {amenity_id} not found")
                    valid_amenities.append(amenity_id)
                place_data['amenity_ids'] = valid_amenities

            # Create place
            place = Place(**place_data)
            self.place_repo.add(place)
            return place
        except Exception as e:
            raise ValueError(f"Error creating place: {str(e)}")

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update existing place"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        try:
            # Update only provided fields
            for key, value in place_data.items():
                if key not in ['id', 'created_at', 'updated_at', 'owner_id']:
                    setattr(place, key, value)

            # Re-validate place
            place.validate()
            self.place_repo.update(place_id, place)
            return place
        except Exception as e:
            raise ValueError(f"Error updating place: {str(e)}")

# Review methods
    def create_review(self, review_data):
        """Create new review"""
        try:
            # Validate required fields
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            for field in required_fields:
                if field not in review_data:
                    raise ValueError(f"{field} is required")

            # Validate user exists
            user = self.get_user(review_data['user_id'])
            if not user:
                raise ValueError(f"User {review_data['user_id']} not found")

            # Validate place exists
            place = self.get_place(review_data['place_id'])
            if not place:
                raise ValueError(f"Place {review_data['place_id']} not found")

            review = Review(**review_data)
            self.review_repo.add(review)
            return review
        except Exception as e:
            raise ValueError(f"Error creating review: {str(e)}")

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        try:
            for key, value in review_data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(review, key, value)
            review.validate()
            self.review_repo.update(review_id, review)
            return review
        except Exception as e:
            raise ValueError(f"Error updating review: {str(e)}")

    def delete_review(self, review_id):
        """Delete a review"""
        if not self.review_repo.get(review_id):
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        try:
            # Vérifie si le place existe
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"Place {place_id} not found")

            # Filtre les reviews pour ce place
            all_reviews = self.get_all_reviews()
            place_reviews = [
                review for review in all_reviews 
                if review.place_id == place_id
            ]
            
            return place_reviews
        except Exception as e:
            raise ValueError(f"Error getting reviews for place: {str(e)}")

facade = HBnBFacade()