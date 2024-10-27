"""Amenity model module for the HBnB application."""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity Model"""
    
    def __init__(self, *args, **kwargs):
        """Initialize amenity"""
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', '')
        self.validate()

    def validate(self):
        """Validate amenity data"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("name cannot be empty")