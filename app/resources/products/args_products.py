"""
File represents args for endpoints of PRODUCTS
"""
from app.resources.utils import type_int_list as int_list
from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('false', '0', 'no'):
        return False
    elif value.lower() in ('true', '1', 'yes'):
        return True
    else:
        raise ValueError('Boolean value expected.')


args_for_products_endpoint = reqparse.RequestParser()

args_for_products_endpoint.add_argument("name", type=str, required=True, help="The name of the product.")
args_for_products_endpoint.add_argument("id_category", type=int, required=True, help="The category id of the product.")
args_for_products_endpoint.add_argument("description", type=str, help="The description of the product.")
args_for_products_endpoint.add_argument("price", type=float, help="The price of the product.")

args_for_products_endpoint.add_argument("stock_quantity", type=int, help="The stock quantity of the product.")
args_for_products_endpoint.add_argument("activated", type=str_to_bool, default='true', help="If product is activated or not.")
args_for_products_endpoint.add_argument(
    'image_thumbnail_name',
    required=True,
    type=FileStorage,
    location="files"
)

args_for_find_products_endpoint = reqparse.RequestParser()

args_for_find_products_endpoint.add_argument(
    "excluded_categories",
    type=int_list,
    required=False,
    help="List of categories IDS to exclude in filter. Example: [1, 2]",
)
args_for_find_products_endpoint.add_argument("query", type=str, required=False, help="Search query")


# update products
args_for_update_products = reqparse.RequestParser()
args_for_update_products.add_argument("name", type=str, required=True, help="The name of the product.")
args_for_update_products.add_argument("id_category", type=int, help="The category id of the product.")
args_for_update_products.add_argument("description", type=str, help="The description of the product.")
args_for_update_products.add_argument("price", type=float, help="The price of the product.")
args_for_update_products.add_argument("stock_quantity", type=int, help="The stock quantity of the product.")
args_for_update_products.add_argument("activated", type=str_to_bool, help="If product is activated or not.")
args_for_update_products.add_argument(
    'image_thumbnail_name',
    type=FileStorage,
    location="files"
)