from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

args_for_images_endpoint = reqparse.RequestParser(bundle_errors=True)


args_for_images_endpoint.add_argument(
    'file',
    required=True,
    type=FileStorage,
    location="files")
args_for_images_endpoint.add_argument(
    "filename",
    required=True,
    type=str,
    location="form"
)
