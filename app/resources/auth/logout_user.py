"""
This module defines the API endpoint for user logout.
"""

from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Resource

from app.blacklist import BLACKLIST
from app.repositories import UserRepository
from . import auth


@auth.route("/logout")
class LogoutUser(Resource):
    """
    Resource class for handling user logout via the '/logout' endpoint.
    """

    user_repository = UserRepository()

    @auth.response(code=200, description="Logged out successfully.")
    @auth.response(code=401, description="Unauthorized access.")
    @jwt_required()
    def post(self):
        """
        Handles POST requests to log out a user.

        This endpoint requires authentication. It revokes the user's JWT token by adding it to the blacklist.

        Returns:
            tuple: A JSON response and an HTTP status code.
                - 200: Logged out successfully.
                - 401: Unauthorized access.
        """
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully"}, 200
