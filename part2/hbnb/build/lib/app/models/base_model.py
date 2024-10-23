from datetime import datetime
import uuid

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour le timestamp updated_at à chaque modification."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs de l'objet avec un dictionnaire."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
