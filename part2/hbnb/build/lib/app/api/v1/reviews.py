"""Review API endpoints"""

from flask import request, current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('review', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True),
    'user_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """List reviews"""
        return current_app.facade.get_all_reviews()

    @api.expect(review_model)
    @api.response(201, 'Review created')
    def post(self):
        """Create review"""
        return current_app.facade.create_review(request.json), 201

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review details"""
        review = current_app.facade.get_review(review_id)
        if not review:
            api.abort(404)
        return review

    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update review"""
        review = current_app.facade.update_review(review_id, request.json)
        if not review:
            api.abort(404)
        return review

    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete review"""
        if current_app.facade.delete_review(review_id):
            return '', 204
        api.abort(404)