"""
Base model providing core functionality for all models.
Common validation and serialization for HBnB models.
"""

import uuid
from typing import Dict, Any
from datetime import datetime


class ValidationError(Exception):
    """Custom validation error"""
    pass


class BaseModel:
    """Base model with ID and validation"""

    def __init__(self, *args, **kwargs):
        """Initialize base model attributes"""
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ['created_at', 'updated_at'] and isinstance(value, str):
                    setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                else:
                    setattr(self, key, value)
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def to_dict(self):
        """Return dictionary representation of the model"""
        result = self.__dict__.copy()
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        result['__class__'] = self.__class__.__name__
        return result

    def validate(self) -> None:
        """
        Base validation method
        Implemented by child classes
        """
        pass

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update model attributes
        Args:
            data: Dictionary of attributes to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate()

    def __str__(self):
        """String representation of the model"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
