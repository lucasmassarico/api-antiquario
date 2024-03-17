"""
File represents args for endpoints of PRODUCTS
"""
from flask_restx import reqparse

args_for_products_endpoint = reqparse.RequestParser()


args_for_products_endpoint.add_argument("name", type=str, required=True, help="The name of the product.")
args_for_products_endpoint.add_argument("id_category", type=int, required=True, help="The category id of the product.")
args_for_products_endpoint.add_argument("description", type=str, help="The description of the product.")
args_for_products_endpoint.add_argument("price", type=float, help="The price of the product.")

args_for_products_endpoint.add_argument("stock_quantity", type=int, help="The stock quantity of the product.")
args_for_products_endpoint.add_argument("activated", type=bool, help="If product is activated or not.")
