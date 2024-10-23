"""
User model implementation for the application
"""

from datetime import datetime
import uuid

class User:
    """User class with basic attributes and validation"""

    def __init__(self, email, password="defaultpassword", first_name="", last_name=""):
        """
        Initialize user instance
        
        Args:
            email: User's email address
            password: User's password (optional, defaults to "defaultpassword")
            first_name: User's first name (optional)
            last_name: User's last name (optional)
        """
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        """
        Convert user to dictionary for API response
        Excludes password and timestamps from response
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

    def validate(self):
        """
        Validate user data
        
        Raises:
            ValueError: If email is invalid
        """
        if not self.email or '@' not in self.email:
            raise ValueError("Valid email required")

    def save(self):
        """Update the timestamp when saving changes"""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """
        Update user attributes
        
        Args:
            data: Dictionary containing fields to update
        """
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.validate()
        self.save()