"""
Implement API endpoints for user management and operations
"""

from flask import request, current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('users', description='User operations')

# API Models
user_model = api.model('UserInput', {
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(required=True, description='User email')
})

user_response = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email')
})

@api.route('/')
class UserList(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        try:
            data = request.json.copy()
            data['password'] = 'defaultpassword'
            user = current_app.facade.create_user(data)
            return user.to_dict(), 200
        except ValueError:
            return {"error": "Invalid input data"}, 400

@api.route('/<string:user_id>')
@api.param('user_id', 'User identifier')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response)
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = current_app.facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_response)
    def put(self, user_id):
        """Update a user"""
        try:
            user = current_app.facade.update_user(user_id, request.json)
            if not user:
                api.abort(404, "User not found")
            return user
        except ValueError as e:
            api.abort(400, str(e))