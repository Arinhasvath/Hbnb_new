"""Amenities API endpoints implementation."""
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Unique identifier'),
    'name': fields.String(required=True, description='Name of the amenity'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

def validate_amenity_name(name):
    if not name or not name.strip():
        raise ValueError("Amenity name cannot be empty")

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return facade.get_all_amenities()

    @api.doc('create_amenity')
    @api.expect(api.model('AmenityInput', {
        'name': fields.String(required=True, description='Name of the amenity')
    }))
    @api.marshal_with(amenity_model, code=201)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new amenity"""
        try:
            validate_amenity_name(api.payload['name'])
            return facade.create_amenity(api.payload), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Fetch an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            api.abort(404, f"Amenity {amenity_id} not found")
        return amenity

    @api.doc('update_amenity')
    @api.expect(api.model('AmenityUpdate', {
        'name': fields.String(required=True, description='New name of the amenity')
    }))
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Validation Error')
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if amenity is None:
                api.abort(404, f"Amenity {amenity_id} not found")
            
            validate_amenity_name(api.payload['name'])
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            return updated_amenity
        except ValueError as e:
            api.abort(400, str(e))