"""
File defining a Flask-RESTx Namespace for testandoImagem CRUD operations.
"""
from flask_restx import Namespace


imagens = Namespace(name="Imagens")

from .create_import_image import UploadImage
