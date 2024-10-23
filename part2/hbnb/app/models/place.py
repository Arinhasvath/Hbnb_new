"""
Place model implementation
"""

from datetime import datetime
import uuid

class Place:
    """Place class with validation"""

    def __init__(self, title, description, owner_id, price, latitude, longitude):
        """Initialize place"""
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.owner_id = owner_id
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner_id': self.owner_id,
            'price': float(self.price),
            'latitude': float(self.latitude),
            'longitude': float(self.longitude)
        }

    def validate(self):
        """Validate place data"""
        if not self.title or not self.description:
            raise ValueError("Title and description are required")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a positive number")
        if not -90 <= float(self.latitude) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= float(self.longitude) <= 180:
            raise ValueError("Longitude must be between -180 and 180")