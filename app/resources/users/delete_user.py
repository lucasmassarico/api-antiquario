# delete_user.py

"""
This module defines the API endpoint for deleting a user.
"""

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.repositories import UserRepository
from . import users


@users.route("/delete/<int:user_id>")
class DeleteUser(Resource):
    """
    Resource class for handling user deletion via the '/delete/<int:user_id>' endpoint.
    """

    user_repository = UserRepository()

    @jwt_required()
    @users.response(code=200, description="User deleted successfully.")
    @users.response(code=401, description="Unauthorized access.")
    @users.response(code=404, description="User not found.")
    @users.response(code=500, description="An error occurred on the server.")
    def delete(self, user_id: int):
        """
        Handles DELETE requests to remove a user from the database.

        This endpoint requires authentication and checks if the logged-in user has administrative privileges.
        It attempts to delete the specified user identified by `user_id`.

        Args:
            user_id (int): The ID of the user to be deleted.

        Returns:
            tuple: A JSON response and an HTTP status code.
                - 200: User deleted successfully.
                - 401: Unauthorized access (not an administrator).
                - 404: User not found.
                - 500: Server error occurred.
        """
        user_logged = self.user_repository.find_user_by_id(user_id=get_jwt_identity())
        if user_logged.access_role != 99:
            return {"message": "You are not an administrator"}, 401

        user = self.user_repository.find_user_by_id(user_id=user_id)
        if not user:
            return {"message": "User not found!"}, 404
        try:
            self.user_repository.delete_user(user)
            return {"message": "User successfully deleted."}, 200
        except Exception as error:
            return {"error": str(error)}, 500
