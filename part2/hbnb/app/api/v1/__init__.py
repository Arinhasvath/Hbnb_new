"""
API v1 package initialization
"""

from app.api.v1.users import api as user_api
from app.api.v1.places import api as place_api
from app.api.v1.reviews import api as review_api
from app.api.v1.amenities import api as amenity_api

__all__ = ['user_api', 'place_api', 'review_api', 'amenity_api']
