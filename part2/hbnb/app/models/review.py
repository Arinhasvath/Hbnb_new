from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review Model"""
    
    def __init__(self, *args, **kwargs):
        """Initialize review"""
        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')
        self.rating = int(kwargs.get('rating', 0))
        self.user_id = kwargs.get('user_id', '')
        self.place_id = kwargs.get('place_id', '')
        self.validate()

    def validate(self):
        """Validate review data"""
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("text cannot be empty")
        if not isinstance(self.rating, (int, float)):
            raise ValueError("rating must be a number")
        try:
            self.rating = int(self.rating)
        except ValueError:
            raise ValueError("rating must be a valid number")
        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.place_id:
            raise ValueError("place_id is required")