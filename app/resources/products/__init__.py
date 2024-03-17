"""
File defining a Flask-RESTx Namespace for Products CRUD operations.
"""
from flask_restx import Namespace


products = Namespace(name="Products", description="Products CRUD")

from .create_product import CreateProduct
from .find_product import FindProductByName, FindAllProducts, FindProductById
from .update_products import UpdateProduct
from .delete_product import DeleteProduct
