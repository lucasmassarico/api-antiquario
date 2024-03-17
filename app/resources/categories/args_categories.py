"""
File represents args for endpoints of PRODUCTS
"""
from flask_restx import reqparse

args_for_categories_endpoint = reqparse.RequestParser()


args_for_categories_endpoint.add_argument("name", type=str, required=True, help="The name of the category.")