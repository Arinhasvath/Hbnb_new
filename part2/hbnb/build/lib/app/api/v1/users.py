"""Users API endpoints"""

from flask import request, current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('user', description='User operations')

user_model = api.model('User', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String(),
    'last_name': fields.String()
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List users"""
        return current_app.facade.get_all_users()

    @api.expect(user_model)
    @api.response(201, 'User created')
    def post(self):
        """Create user"""
        return current_app.facade.create_user(request.json), 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get user details"""
        user = current_app.facade.get_user(user_id)
        if not user:
            api.abort(404)
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update user"""
        user = current_app.facade.update_user(user_id, request.json)
        if not user:
            api.abort(404)
        return user