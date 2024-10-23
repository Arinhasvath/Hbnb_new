"""
Place API endpoints implementation
"""

from flask import request, current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Place latitude'),
    'longitude': fields.Float(required=True, description='Place longitude')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        try:
            place = current_app.facade.create_place(request.json)
            return place.to_dict(), 200
        except ValueError:
            return {"error": "Invalid input data"}, 400