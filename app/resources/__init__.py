"""
Module defining a function for initializing Flask-RESTx namespaces within a Flask application.

This module includes a function 'init_app' that adds multiple namespaces to a Flask-RESTx API instance.
"""
from app.resources.products import products as products_ns
from app.resources.categories import categories as categories_ns
from app.resources.auth import auth as auth_ns
from app.resources.users import users as users_ns
from app.resources.sold_products import sold_products as sold_products_ns

from app.resources.imagensToProducts import imagens_for_products as imagens_ns


def init_app(api):
    """
    Initialize Flask-RESTx namespaces within a Flask application.
    """
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(products_ns, path="/products")
    api.add_namespace(imagens_ns, path="/products_images")
    api.add_namespace(categories_ns, path="/categories")
    api.add_namespace(sold_products_ns, path="/sold_products")
