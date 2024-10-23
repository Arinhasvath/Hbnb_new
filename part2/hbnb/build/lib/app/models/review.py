"""Review model module"""

from datetime import datetime
import uuid

class Review:
    def __init__(self, text, rating, place_id, user_id):
        self.id = str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.place = None
        self.user = None
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': int(self.rating),
            'place_id': self.place_id,
            'user_id': self.user_id,
            'place': self.place.to_dict() if self.place else None,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def validate(self):
        if not self.text:
            raise ValueError("Review text required")
        if not isinstance(self.rating, (int)) or not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")