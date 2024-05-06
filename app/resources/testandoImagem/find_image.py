import os
from flask import render_template, make_response
from flask_restx import Resource

from . import imagens

UPLOAD_FOLDER = 'uploads'

@imagens.route("/get/<filename>")
class FindImage(Resource):
    def get(self, filename: str):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print("Caminho do arquivo:", file_path)
        if os.path.isfile(file_path):
            headers = {
                'Content-Type': 'text/html'
            }
            return make_response(
                render_template(
                    "image.html",
                    file_path=file_path,
                    image_name=filename
                ),
                200,
                headers
            )
        else:
            return {"message": "Image nao encontrada"}, 404
