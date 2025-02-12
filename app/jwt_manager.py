"""
Module configuring and defining JWT-related functions for user authentication.

This module includes a Flask JWT Manager instance and functions for handling token-related operations,
such as checking if a token is in the blacklist, handling revoked tokens, and looking up users based on token data.
"""
from flask import jsonify
from flask_jwt_extended import JWTManager

from app.blacklist import BLACKLIST

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_blacklist(self, token):
    """
    Check if a JWT token is in the blacklist.

    Parameters:
    - token (dict): The JWT token to be checked.

    Returns:
    - bool: True if the token is in the blacklist, False otherwise.
    """
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalid_access_token(jwt_header, jwt_payload):
    """
    Handle revoked JWT access tokens.

    Parameters:
    - jwt_header (dict): The header of the JWT token.
    - jwt_payload (dict): The payload of the JWT token.

    Returns:
    - Response: A JSON response indicating that the user has been logged out.
      The response includes a message and a 401 status code.
    """
    return jsonify({"message": "You have been logged out."}), 401


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Register a callback function that loads a user from your database whenever
    a protected route is accessed. This should return any python object on a
    successful lookup, or None if the lookup failed for any reason (for example
    if the user has been deleted from the database).
    """
    from app.repositories import UserRepository

    identity = jwt_data["sub"]

    user_repository = UserRepository()
    user = user_repository.find_user_by_id(user_id=identity)

    if user:
        return user
    return None
