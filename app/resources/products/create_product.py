"""
This file contains Flask-RESTx resources for "post" product-related operations.
"""
from flask_restx import Resource
from app.models.product import ProductModel
from app.repositories import ProductRepository

from . import products
from .args_products import args_for_products_endpoint as args_params
from app.resources.utils import allowed_file, PRODUCT_UPLOAD_PATH

import os


@products.route("/create")
class CreateProduct(Resource):
    product_repository = ProductRepository()

    @products.expect(args_params)
    @products.response(code=201, description="Product created successfully.")
    @products.response(code=400, description="The provided category ID is not associated with any existing category.")
    @products.response(code=409, description="Product name conflict. The provided product name already exists in the database.")
    @products.response(code=500, description="Error in server as occurred.")
    def post(self):
        """
        Endpoint to create a new product.
        """
        data = args_params.parse_args()
        data['name'] = data['name'].upper()

        if self.product_repository.find_products_by_name(product_name=data['name']):
            return {"error": f"The product name '{data['name']}' already exists in the database."}, 409

        errors = self.product_repository.check_category_existence(category_id=data['id_category'])
        if errors:
            return {"errors": errors}, 400

        # salvar thumbnail do produto
        image_file = data['image_thumbnail_name']
        image_filename = image_file.filename
        file_extension = image_filename.split('.')[-1].lower()

        # necessita tirar ele do dicionário do data, pois precisamos tratar o path a ser salvo
        data.pop('image_thumbnail_name', None)

        product = ProductModel(**data)

        if not allowed_file(image_filename):
            return {"error": "file not allowed extension."}, 400

        try:
            self.product_repository.add_product(product=product)

            # cria pasta do produto, sendo a pasta padrão dos produtos, "product/product_id"
            product_folder = f"{PRODUCT_UPLOAD_PATH}/{product.id}"
            os.makedirs(product_folder, exist_ok=True)

            # adiciona a thumbnail a essa pasta
            path = os.path.join(product_folder, f"{str(product.id)}_thumbnail.{file_extension}")
            image_file.save(path)

            relative_path = os.path.relpath(path, 'app/static/public').replace("\\", "/")

            # adiciona ao data e atualiza o produto
            data['image_thumbnail_name'] = f"public/{relative_path}"
            self.product_repository.update_product(product=product, **data)

            return self.product_repository.json(product=product), 201
        except Exception as error:
            return {"error": error}, 500
