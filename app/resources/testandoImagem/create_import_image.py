import os
from flask_restx import Resource

from . import imagens
from .args_imagens import args_for_images_endpoint as args_params

UPLOAD_FOLDER = 'uploads'

@imagens.route("/upload")
class UploadImage(Resource):
    @imagens.expect(args_params)
    def post(self):
        args = args_params.parse_args()
        image = args.file
        # image.save(args.filename)
        image.save(os.path.join('uploads', args.filename))
