from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place Model"""
    
    def __init__(self, *args, **kwargs):
        """Initialize place"""
        super().__init__(*args, **kwargs)
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.price = kwargs.get('price', 0)
        self.latitude = kwargs.get('latitude', 0)
        self.longitude = kwargs.get('longitude', 0)
        self.owner_id = kwargs.get('owner_id', '')
        self.amenity_ids = kwargs.get('amenity_ids', [])
        self.validate()  # Validation lors de l'initialisation

    def validate(self):
        """Validate place data"""
        # Required fields validation
        required_fields = ['title', 'description', 'owner_id']
        for field in required_fields:
            value = getattr(self, field)
            if not value or (isinstance(value, str) and len(value.strip()) == 0):
                raise ValueError(f"{field} cannot be empty")

        # Price validation
        if not isinstance(self.price, (int, float)):
            raise ValueError("price must be a number")
        if self.price < 0:
            raise ValueError("price cannot be negative")
        
        # Coordinates validation
        if not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number")
        if not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number")
        
        if self.latitude < -90 or self.latitude > 90:
            raise ValueError("latitude must be between -90 and 90")
        if self.longitude < -180 or self.longitude > 180:
            raise ValueError("longitude must be between -180 and 180")

        # Amenities validation
        if not isinstance(self.amenity_ids, list):
            raise ValueError("amenity_ids must be a list")
        
        return True

    def to_dict(self):
        """Return dictionary representation"""
        place_dict = super().to_dict()
        place_dict['price'] = float(self.price)  # Ensure price is float
        return place_dict