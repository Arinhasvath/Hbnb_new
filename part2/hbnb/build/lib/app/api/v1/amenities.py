"""Amenity API endpoints"""

from flask import request, current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('amenity', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List amenities"""
        return current_app.facade.get_all_amenities()

    @api.expect(amenity_model)
    @api.response(201, 'Amenity created')
    def post(self):
        """Create amenity"""
        return current_app.facade.create_amenity(request.json), 201

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity details"""
        amenity = current_app.facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404)
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update amenity"""
        amenity = current_app.facade.update_amenity(amenity_id, request.json)
        if not amenity:
            api.abort(404)
        return amenity