"""
This file contains Flask-RESTx resources for "put" products-related operations.
"""
import os
from flask_restx import Resource
from app.repositories import ProductRepository
from . import products
from . args_products import args_for_update_products as args_params
from app.resources.utils import allowed_file, PRODUCT_UPLOAD_PATH


@products.route("/update/<int:product_id>")
class UpdateProduct(Resource):
    product_repository = ProductRepository()

    @products.expect(args_params)
    @products.response(code=200, description="Product updated successfully.")
    @products.response(code=400, description="The provided category ID is not associated with any existing category.")
    @products.response(code=404, description="Product not found.")
    @products.response(code=409, description="Product name conflict. The provided product name already exists in the database.")
    @products.response(code=500, description="Error in server as occurred.")
    def put(self, product_id: int):
        """
        Endpoint to update an existing product by id.
        """
        data = args_params.parse_args()
        data['name'] = data['name'].upper()

        product_by_name = self.product_repository.find_products_by_name(product_name=data['name'])
        if product_by_name and product_by_name.id != product_id:
            return {"error": f"The name '{data['name']}' is registered in another product."}, 409

        # Verifica a categoria
        if data['id_category']:
            errors = self.product_repository.check_category_existence(category_id=data['id_category'])
            if errors:
                return {"errors": errors}, 400

        # Procura o produto
        product_found = self.product_repository.find_product_by_id(product_id=product_id)
        if not product_found:
            return {"error": f"Product '{product_id}' not registered."}, 404

        try:
            # Atualização dos campos
            if not data['name']:
                data['name'] = product_found.name

            if not data['id_category']:
                data['id_category'] = product_found.id_category

            if not data['description']:
                data['description'] = product_found.description

            if not data['price']:
                data['price'] = product_found.price

            if not data['stock_quantity']:
                data['stock_quantity'] = product_found.stock_quantity

            if 'activated' not in data or data['activated'] is None:
                data['activated'] = product_found.activated

            # Atualização da imagem (se fornecida)
            image_file = data.get('image_thumbnail_name', None)
            if image_file:
                image_filename = image_file.filename
                file_extension = image_filename.split('.')[-1].lower()

                if not allowed_file(image_filename):
                    return {"error": "file not allowed extension."}, 400

                # Diretório do produto
                product_folder = f"{PRODUCT_UPLOAD_PATH}/{product_found.id}"

                # Cria o diretório do produto, caso não exista
                os.makedirs(product_folder, exist_ok=True)

                # Define o caminho do arquivo, mantendo o mesmo nome de arquivo
                path = os.path.join(product_folder, f"{str(product_found.id)}_thumbnail.{file_extension}")

                # Remove a imagem anterior (opcional)
                if os.path.exists(path):
                    os.remove(path)

                # Salva a nova imagem
                image_file.save(path)

                # Atualiza o campo de imagem no produto
                relative_path = os.path.relpath(path, 'app/static/public').replace("\\", "/")
                data['image_thumbnail_name'] = f"public/{relative_path}"

            else:
                # Se nenhuma imagem nova foi fornecida, mantém a existente
                data['image_thumbnail_name'] = product_found.image_thumbnail_name

            # Atualiza o produto
            self.product_repository.update_product(product=product_found, **data)

            return self.product_repository.json(product=product_found), 200

        except Exception as error:
            return {"error": str(error)}, 500
