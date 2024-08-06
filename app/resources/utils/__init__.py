import json
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PRODUCT_UPLOAD_PATH = os.environ['PRODUCT_IMAGES_PATH']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'tiff'}


# def create_product_folder(product_id: int):
#     """
#     Check if folder exist or nothing.
#     """
#     product_folder = os.path.join(UPLOAD_FOLDER, str(product_id))
#     if not os.path.exists(product_folder):
#         os.makedirs(product_folder)


def allowed_file(filename):
    return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def type_int_list(value):
    try:
        values = json.loads(value)
        if isinstance(values, list) and all(isinstance(i, int) for i in values):
            return values
        else:
            raise ValueError("List must contain only integers.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
