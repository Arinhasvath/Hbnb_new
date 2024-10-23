"""Places API endpoints"""

from flask import request, current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('place', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String)
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """List places"""
        return current_app.facade.get_all_places()

    @api.expect(place_model)
    @api.response(201, 'Place created')
    def post(self):
        """Create place"""
        return current_app.facade.create_place(request.json), 201

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get place details"""
        place = current_app.facade.get_place(place_id)
        if not place:
            api.abort(404)
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update place"""
        place = current_app.facade.update_place(place_id, request.json)
        if not place:
            api.abort(404)
        return place