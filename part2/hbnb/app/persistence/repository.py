# app/services/facade.py
from typing import Dict, List, Optional, TypeVar, Generic, Type
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
import json
import os

T = TypeVar('T', bound=BaseModel)

class InMemoryRepository(Generic[T]):
    """
    Generic in-memory repository implementing basic CRUD operations.
    Uses dictionary as storage backend.
    """
    def __init__(self, entity_class: Type[T]):
        self._storage: Dict[str, T] = {}
        self._storage_file = f'{entity_class.__name__.lower()}_data.json'
        self._entity_class = entity_class
        self._load()
    def _load(self):  # Méthode correctement indentée
        try:
            if os.path.exists(self._storage_file):
                with open(self._storage_file, 'r') as f:
                    data = json.load(f)
                    self._storage = {k: self._deserialize(v) for k, v in data.items()}
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            self._storage = {}

    def _save(self):
        try:
            data = {k: v.to_dict() for k, v in self._storage.items()}
            with open(self._storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise ValueError(f"Error saving data: {str(e)}")

    def add(self, entity: T) -> None:
        if hasattr(entity, 'id'):
            if entity.id in self._storage:
                raise ValueError(f"Entity with id {entity.id} already exists")
            self._storage[entity.id] = entity
        else:
            raise ValueError("Entity must have an id attribute")
        self._save()

    def get(self, entity_id: str) -> Optional[T]:
        return self._storage.get(entity_id)

    def get_all(self) -> List[T]:
        return list(self._storage.values())

    def update(self, entity_id: str, entity: T) -> None:
        if entity_id not in self._storage:
            raise ValueError(f"Entity with id {entity_id} not found")
        self._storage[entity_id] = entity
        self._save()

    def delete(self, entity_id: str) -> None:
        if entity_id not in self._storage:
            raise ValueError(f"Entity with id {entity_id} not found")
        del self._storage[entity_id]
        self._save()

    def _deserialize(self, data: Dict) -> T:
        if self._entity_class and issubclass(self._entity_class, BaseModel):
            return self._entity_class(**data)
        else:
            raise ValueError(f"Cannot deserialize data for unknown entity type")
        
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository(User)
        self.place_repo = InMemoryRepository(Place)
        self.amenity_repo = InMemoryRepository(Amenity)
        self.review_repo = InMemoryRepository(Review)

    # User methods
    def create_user(self, user_data):
        try:
            user = User(**user_data)
            self.user_repo.add(user)
            return user
        except ValueError as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def get_user(self, user_id: str):
        try:
            return self.user_repo.get(user_id)
        except ValueError as e:
            raise ValueError(f"Error retrieving user: {str(e)}")

    def get_all_users(self):
        try:
            return self.user_repo.get_all()
        except ValueError as e:
            raise ValueError(f"Error retrieving users: {str(e)}")

    def update_user(self, user_id: str, user_data: dict):
        try:
            user = self.get_user(user_id)
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                self.user_repo.update(user_id, user)
                return user
            return None
        except ValueError as e:
            raise ValueError(f"Error updating user: {str(e)}")

    # Place methods
    def create_place(self, place_data):
        try:
            place = Place(**place_data)
            self.place_repo.add(place)
            return place
        except ValueError as e:
            raise ValueError(f"Error creating place: {str(e)}")

    def get_place(self, place_id: str):
        try:
            return self.place_repo.get(place_id)
        except ValueError as e:
            raise ValueError(f"Error retrieving place: {str(e)}")

    def get_all_places(self):
        try:
            return self.place_repo.get_all()
        except ValueError as e:
            raise ValueError(f"Error retrieving places: {str(e)}")

    def update_place(self, place_id: str, place_data: dict):
        try:
            place = self.get_place(place_id)
            if place:
                for key, value in place_data.items():
                    setattr(place, key, value)
                self.place_repo.update(place_id, place)
                return place
            return None
        except ValueError as e:
            raise ValueError(f"Error updating place: {str(e)}")

    # Amenity methods
    def create_amenity(self, amenity_data):
        try:
            amenity = Amenity(**amenity_data)
            self.amenity_repo.add(amenity)
            return amenity
        except ValueError as e:
            raise ValueError(f"Error creating amenity: {str(e)}")

    def get_amenity(self, amenity_id: str):
        try:
            return self.amenity_repo.get(amenity_id)
        except ValueError as e:
            raise ValueError(f"Error retrieving amenity: {str(e)}")

    def get_all_amenities(self):
        try:
            return self.amenity_repo.get_all()
        except ValueError as e:
            raise ValueError(f"Error retrieving amenities: {str(e)}")

    def update_amenity(self, amenity_id: str, amenity_data: dict):
        try:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                for key, value in amenity_data.items():
                    setattr(amenity, key, value)
                self.amenity_repo.update(amenity_id, amenity)
                return amenity
            return None
        except ValueError as e:
            raise ValueError(f"Error updating amenity: {str(e)}")

    # Review methods
    def create_review(self, review_data):
        try:
            review = Review(**review_data)
            self.review_repo.add(review)
            return review
        except ValueError as e:
            raise ValueError(f"Error creating review: {str(e)}")

    def get_review(self, review_id: str):
        try:
            return self.review_repo.get(review_id)
        except ValueError as e:
            raise ValueError(f"Error retrieving review: {str(e)}")

    def get_all_reviews(self):
        try:
            return self.review_repo.get_all()
        except ValueError as e:
            raise ValueError(f"Error retrieving reviews: {str(e)}")

    def get_reviews_by_place(self, place_id: str):
        try:
            return [review for review in self.get_all_reviews()
                if review.place_id == place_id]
        except ValueError as e:
            raise ValueError(f"Error retrieving reviews for place: {str(e)}")

    def update_review(self, review_id: str, review_data: dict):
        try:
            review = self.get_review(review_id)
            if review:
                for key, value in review_data.items():
                    setattr(review, key, value)
                self.review_repo.update(review_id, review)
                return review
            return None
        except ValueError as e:
            raise ValueError(f"Error updating review: {str(e)}")

    def delete_review(self, review_id: str):
        try:
            self.review_repo.delete(review_id)
        except ValueError as e:
            raise ValueError(f"Error deleting review: {str(e)}")