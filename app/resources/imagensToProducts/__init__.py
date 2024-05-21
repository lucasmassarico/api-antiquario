"""
File defining a Flask-RESTx Namespace for imagensToProducts CRUD operations.
"""
from flask_restx import Namespace


imagens_for_products = Namespace(name="Products Images")

from .create_import_image import UploadImage
from .find_product_image import FindProductImage
