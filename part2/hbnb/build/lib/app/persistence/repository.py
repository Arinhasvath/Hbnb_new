"""
In-memory repository implementation for the HBnB application.
Provides temporary storage and basic CRUD operations.
Will be replaced by SQLAlchemy in Part 3.
"""

from typing import Dict, List, Optional, TypeVar, Generic

T = TypeVar('T')

class InMemoryRepository(Generic[T]):
    """
    Generic in-memory repository implementing basic CRUD operations.
    Uses dictionary as storage backend.
    """

    def __init__(self):
        """
        Initialize empty storage.
        """
        self._storage: Dict[str, T] = {}

    def add(self, entity: T) -> None:
        """
        Add new entity to storage.
        
        Args:
            entity: Entity to store, must have id attribute
            
        Raises:
            ValueError: If entity with same id already exists
        """
        if hasattr(entity, 'id'):
            if entity.id in self._storage:
                raise ValueError(f"Entity with id {entity.id} already exists")
            self._storage[entity.id] = entity
        else:
            raise ValueError("Entity must have an id attribute")

    def get(self, entity_id: str) -> Optional[T]:
        """
        Retrieve entity by id.
        
        Args:
            entity_id: ID of entity to retrieve
            
        Returns:
            Entity if found, None otherwise
        """
        return self._storage.get(entity_id)

    def get_all(self) -> List[T]:
        """
        Retrieve all entities.
        
        Returns:
            List of all stored entities
        """
        return list(self._storage.values())

    def update(self, entity_id: str, entity: T) -> None:
        """
        Update existing entity.
        
        Args:
            entity_id: ID of entity to update
            entity: Updated entity data
            
        Raises:
            ValueError: If entity doesn't exist
        """
        if entity_id not in self._storage:
            raise ValueError(f"Entity with id {entity_id} not found")
        self._storage[entity_id] = entity

    def delete(self, entity_id: str) -> None:
        """
        Remove entity from storage.
        
        Args:
            entity_id: ID of entity to delete
            
        Raises:
            ValueError: If entity doesn't exist
        """
        if entity_id not in self._storage:
            raise ValueError(f"Entity with id {entity_id} not found")
        del self._storage[entity_id]

    def get_by_attribute(self, attr_name: str, attr_value: any) -> Optional[T]:
        """
        Find first entity matching attribute value.
        
        Args:
            attr_name: Name of attribute to match
            attr_value: Value to match against
            
        Returns:
            Matching entity if found, None otherwise
        """
        for entity in self._storage.values():
            if hasattr(entity, attr_name) and getattr(entity, attr_name) == attr_value:
                return entity
        return None
