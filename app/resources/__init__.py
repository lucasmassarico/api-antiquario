"""
Module defining a function for initializing Flask-RESTx namespaces within a Flask applciation.

This module includes a function 'init_app' that adds multiple namespaces to a Flask-RESTx API instance.
"""
from app.resources.products import products as products_ns
from app.resources.categories import categories as categories_ns

from app.resources.imagensToProducts import imagens_for_products as imagens_ns


def init_app(api):
    """
    Initialize Flask-RESTx namespaces within a Flask application.
    """
    api.add_namespace(products_ns, path="/products")
    api.add_namespace(categories_ns, path="/categories")
    api.add_namespace(imagens_ns, path="/products_images")
