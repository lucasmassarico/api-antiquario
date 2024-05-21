import os
import re
from flask_restx import Resource

from . import imagens_for_products
from app.repositories import ProductRepository, ProductImagesRepository
from app.models.product import ProductImagesModel

from .args_imagens import args_for_createImages_endpoint as argsParams
from app.resources.utils import allowed_file, PRODUCT_UPLOAD_PATH


@imagens_for_products.route("/upload/by_product_id")
class UploadImage(Resource):
    product_repository = ProductRepository()
    product_images_repository = ProductImagesRepository()

    @imagens_for_products.expect(argsParams)
    def post(self):
        """
        Endpoint to create a product image in server by id.
        """
        data = argsParams.parse_args()

        # tratamento das imagens
        image_file = data['file']
        image_filename = image_file.filename
        file_extension = image_filename.split('.')[-1].lower()

        if not allowed_file(image_filename):
            return {"error": "file not allowed extension."}, 400

        product = self.product_repository.find_product_by_id(product_id=data['id_product'])

        if not product:
            return {"error": "Product not found."}, 404

        # pegar o número do produto, e procurar a pasta dele
        # se a pasta existir ok, se não, cria
        product_folder = f"{PRODUCT_UPLOAD_PATH}/{product.id}"
        os.makedirs(product_folder, exist_ok=True)

        # encontra todos os arquivos da pasta do produto
        existing_files = os.listdir(product_folder)

        # Define o padrão de regex para encontrar o sufixo numérico dos arquivos
        pattern = re.compile(rf"pd_{product.id}_(\d+)\.{file_extension}")

        # Encontra o maior número de sufixo
        max_index = 0
        for file in existing_files:
            match = pattern.match(file)
            if match:
                index = int(match.group(1))
                if index > max_index:
                    max_index = index

        next_index = max_index + 1
        new_filename = f"pd_{product.id}_{next_index}.{file_extension}"
        new_filepath = os.path.join(product_folder, new_filename)

        image_file.save(new_filepath)

        # Verifica se o arquivo foi criado com sucesso
        if not os.path.exists(new_filepath):
            return {"error": "error occurred when try to save image."}, 500
        # Caminho relativo a ser salvo no banco de dados
        relative_path = f"public/products/{product.id}/{new_filename}"

        data.pop('file')
        data['image_path'] = relative_path

        product_images = ProductImagesModel(**data)

        self.product_images_repository.add_product_image(product_images)

        return self.product_images_repository.json(product_images), 201
