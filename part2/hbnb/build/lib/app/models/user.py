"""User model module"""

from datetime import datetime
import uuid

class User:
    def __init__(self, email, password, first_name="", last_name=""):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def validate(self):
        if not self.email or '@' not in self.email:
            raise ValueError("Valid email required")
        if not self.password or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")

    def save(self):
        self.updated_at = datetime.utcnow()

    def update(self, data):
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.validate()
        self.save()