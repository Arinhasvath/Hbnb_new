"""Amenity model module"""

from datetime import datetime
import uuid

class Amenity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def validate(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Name required and must not exceed 50 chars")