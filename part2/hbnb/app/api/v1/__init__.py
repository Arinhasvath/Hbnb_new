"""
API v1 package initialization
"""
from flask_restx import Api

api = Api(
    title='HBnB API',
    version='1.0',
    description='HBnB Application API'
)

from .users import api as users_ns
from .places import api as places_ns
from .amenities import api as amenities_ns
from .reviews import api as reviews_ns

api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(reviews_ns, path='/api/v1/reviews')

__all__ = ['user_api', 'place_api', 'review_api', 'amenity_api']
