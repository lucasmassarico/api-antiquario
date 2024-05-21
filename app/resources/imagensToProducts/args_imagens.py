from flask_restx import reqparse
from werkzeug.datastructures import FileStorage
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


args_for_createImages_endpoint = reqparse.RequestParser(bundle_errors=True)
args_for_createImages_endpoint.add_argument("id_product", type=int, required=True, help="The id of the product.")
args_for_createImages_endpoint.add_argument(
    'file',
    required=True,
    type=FileStorage,
    location="files"
)
