"""Flask application factory"""

from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

def create_app():
    """Create Flask application"""
    app = Flask(__name__)

    # Create API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB REST API'
    )

    # Initialize Facade
    app.facade = HBnBFacade()  # Cette ligne manquait

    # Register namespaces
    from app.api.v1.places import api as place_api
    from app.api.v1.reviews import api as review_api
    from app.api.v1.amenities import api as amenity_api
    from app.api.v1.users import api as user_api

    api.add_namespace(place_api, path='/api/v1/places')
    api.add_namespace(review_api, path='/api/v1/reviews')
    api.add_namespace(amenity_api, path='/api/v1/amenities')
    api.add_namespace(user_api, path='/api/v1/users')
    return app
