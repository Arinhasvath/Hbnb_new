"""Place model module"""

from datetime import datetime
import uuid

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.owner = None
        self.amenities = []
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'amenities': [a.to_dict() for a in self.amenities],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def validate(self):
        if not self.title or len(self.title) > 100:
            raise ValueError("Title required and must not exceed 100 chars")
        if not self.description:
            raise ValueError("Description required")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be positive number")
        if not -90 <= float(self.latitude) <= 90:
            raise ValueError("Invalid latitude")
        if not -180 <= float(self.longitude) <= 180:
            raise ValueError("Invalid longitude")