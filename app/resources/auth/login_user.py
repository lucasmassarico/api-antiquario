"""
This module defines the API endpoint for user login.
"""

from flask_jwt_extended import create_access_token
from flask_restx import Resource, reqparse
from werkzeug.security import check_password_hash

from app.repositories import UserRepository
from . import auth


@auth.route("/login")
class LoginUser(Resource):
    """
    Resource class for handling user login via the '/login' endpoint.
    """

    user_repository = UserRepository()

    args = reqparse.RequestParser()
    args.add_argument(
        "email",
        type=str,
        required=True,
        help="Email address cannot be blank.",
    )
    args.add_argument(
        "password",
        type=str,
        required=True,
        help="Password cannot be blank.",
    )

    @auth.response(code=200, description="Access token successfully generated.")
    @auth.response(code=401, description="Invalid credentials.")
    @auth.expect(args)
    def post(self):
        """
        Handles POST requests for user login.

        Parses the user's email and password, authenticates the user, and returns an access token if successful.

        Returns:
            tuple: A JSON response containing the access token and an HTTP status code.
        """
        data = self.args.parse_args()

        user = self.user_repository.find_user_by_email(email=data['email'])
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        return {"message": "The email or password is incorrect."}, 401
