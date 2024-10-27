"""Places API endpoints implementation."""
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Unique identifier'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude location'),
    'longitude': fields.Float(required=True, description='Longitude location'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.get_all_places()

    @api.doc('create_place')
    @api.expect(api.model('PlaceInput', {
        'title': fields.String(required=True),
        'description': fields.String(required=True),
        'price': fields.Float(required=True),
        'latitude': fields.Float(required=True),
        'longitude': fields.Float(required=True),
        'owner_id': fields.String(required=True),
        'amenity_ids': fields.List(fields.String)
    }))
    @api.marshal_with(place_model, code=201)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new place"""
        try:
            return facade.create_place(api.payload), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Fetch a place by ID"""
        place = facade.get_place(place_id)
        if place is None:
            api.abort(404, f"Place {place_id} not found")
        return place

    @api.doc('update_place')
    @api.expect(api.model('PlaceUpdate', {
        'title': fields.String(),
        'description': fields.String(),
        'price': fields.Float(),
        'latitude': fields.Float(),
        'longitude': fields.Float(),
        'amenity_ids': fields.List(fields.String)
    }))
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update a place"""
        try:
            place = facade.update_place(place_id, api.payload)
            if place is None:
                api.abort(404, f"Place {place_id} not found")
            return place
        except ValueError as e:
            api.abort(400, str(e))