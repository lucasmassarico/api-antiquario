"""
This module defines the API endpoints for retrieving user information.
"""

from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user
from app.repositories import UserRepository
from . import users


@users.route('/find/by_id/<int:user_id>')
class FindUserById(Resource):
    """
    Resource class for handling user retrieval by user ID via the '/find/by_id/<int:user_id>' endpoint.
    """

    user_repository = UserRepository()

    @users.response(code=200, description="User successfully found.")
    @users.response(code=401, description="Unauthorized access.")
    @users.response(code=404, description="User not found.")
    @jwt_required()
    def get(self, user_id: int):
        """
        Handles GET requests to retrieve a user by their ID.

        This endpoint requires authentication and checks if the logged-in user has administrative privileges.
        It attempts to retrieve the user identified by `user_id`.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            tuple: A JSON response and an HTTP status code.
                - 200: User successfully found.
                - 401: Unauthorized access (not an administrator).
                - 404: User not found.
        """
        if current_user.access_role != 99:
            return {"message": "You are not an administrator"}, 401

        user = self.user_repository.find_user_by_id(user_id=user_id)
        if user:
            return self.user_repository.json(user=user), 200
        return {"message": "User not found."}, 404


@users.route('/find/by_email/<string:email>')
class FindUserByEmail(Resource):
    """
    Resource class for handling user retrieval by email via the '/find/by_email/<string:email>' endpoint.
    """

    user_repository = UserRepository()

    @users.response(code=200, description="User successfully found.")
    @users.response(code=401, description="Unauthorized access.")
    @users.response(code=404, description="User not found.")
    @jwt_required()
    def get(self, email: str):
        """
        Handles GET requests to retrieve a user by their email address.

        This endpoint requires authentication and checks if the logged-in user has administrative privileges.
        It attempts to retrieve the user identified by `email`.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            tuple: A JSON response and an HTTP status code.
                - 200: User successfully found.
                - 401: Unauthorized access (not an administrator).
                - 404: User not found.
        """
        if current_user.access_role != 99:
            return {"message": "You are not an administrator"}, 401

        user = self.user_repository.find_user_by_email(email=email)
        if user:
            return self.user_repository.json(user=user), 200
        return {"message": "User not found."}, 404


@users.route('/find/all')
class FindAllUser(Resource):
    """
    Resource class for handling retrieval of all users via the '/find/all' endpoint.
    """

    user_repository = UserRepository()

    @users.response(code=200, description="Users successfully found.")
    @users.response(code=401, description="Unauthorized access.")
    @users.response(code=500, description="An error occurred on the server.")
    @jwt_required()
    def get(self):
        """
        Handles GET requests to retrieve all users.

        This endpoint requires authentication and checks if the logged-in user has administrative privileges.
        It attempts to retrieve all users from the database.

        Returns:
            tuple: A JSON response and an HTTP status code.
                - 200: Users successfully found.
                - 401: Unauthorized access (not an administrator).
                - 500: Server error occurred.
        """
        if current_user.access_role != 99:
            return {"message": "You are not an administrator"}, 401

        try:
            all_users = self.user_repository.find_all_users()
            users_to_json = [self.user_repository.json(user=user) for user in all_users]
            return users_to_json, 200
        except Exception as error:
            return {"error": str(error)}, 500
