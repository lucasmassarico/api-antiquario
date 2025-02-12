"""
This module defines the request parsers for the 'users' resource,
specifying the expected arguments for user-related API endpoints.
"""

from flask_restx import reqparse, inputs

args = reqparse.RequestParser()

args.add_argument(
    "name",
    type=str,
    required=True,
    help="User's full name. Maximum 100 characters.",
)

args.add_argument(
    "email",
    type=str,
    required=True,
    help="User's email address. Maximum 150 characters.",
)

args.add_argument(
    "password",
    type=str,
    required=True,
    help="User's password. Maximum 255 characters.",
)

args.add_argument(
    "active",
    type=inputs.boolean,
    required=False,
    default=True,
    help="User's active status. Set to True if the account is active; defaults to True.",
)

args.add_argument(
    "access_role",
    type=int,
    required=False,
    default=1,
    help="User's access role level. Defaults to 1.",
)
