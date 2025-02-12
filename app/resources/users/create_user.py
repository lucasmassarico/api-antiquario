"""
This module defines the API endpoint for creating a new user.
"""

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.security import generate_password_hash

from app.models.user import UserModel
from app.repositories import UserRepository
from . import users
from .args import args


@users.route('/create')
class CreateUser(Resource):
    """
    Resource class for handling user creation via the '/create' endpoint.
    """

    user_repository = UserRepository()

    @jwt_required()
    @users.expect(args)
    @users.response(code=201, description="User created successfully.")
    @users.response(code=400, description="Email already registered.")  # bad request
    @users.response(code=401, description="Unauthorized access.")
    @users.response(code=500, description="An error occurred on the server.")
    def post(self):
        """
        Handles POST requests to create a new user.

        This endpoint requires authentication and checks if the logged-in user has administrative privileges.
        It parses the request arguments, validates them, and attempts to create a new user in the database.

        Returns:
            tuple: A JSON response and an HTTP status code.
                - 201: User created successfully.
                - 400: Email already registered.
                - 401: Unauthorized access (not an administrator).
                - 500: Server error occurred.
        """
        data = args.parse_args()
        data["name"] = data["name"].lower()
        data["email"] = data["email"].lower()

        user_logged = self.user_repository.find_user_by_id(user_id=get_jwt_identity())
        if user_logged.access_role != 99:
            return {"error": "You are not an administrator"}, 401

        if self.user_repository.find_user_by_email(data["email"]):
            return {"message": f"The email '{data['email']}' is already registered."}, 400

        user = UserModel(**data)
        user.password = generate_password_hash(user.password)

        try:
            self.user_repository.add_user(user=user)
            return self.user_repository.json(user=user), 201
        except Exception as error:
            return {"error": str(error)}, 500
