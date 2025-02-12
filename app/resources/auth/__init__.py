"""
This module initializes the 'auth' namespace for authentication-related endpoints.
It imports and registers the authentication resources for user login and logout.
"""

from flask_restx import Namespace

auth = Namespace(name="Auth", description="Authentication endpoints for the API.")

from .login_user import LoginUser
from .logout_user import LogoutUser
