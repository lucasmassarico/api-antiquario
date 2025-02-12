"""
This file contains Flask-RESTx resources for "delete" product-related operations.
"""
import os
import shutil
from flask_restx import Resource
from app.repositories import ProductRepository

from . import products
from app.resources.utils import PRODUCT_UPLOAD_PATH


@products.route("/delete/<int:product_id>")
class DeleteProduct(Resource):
    product_repository = ProductRepository()

    @products.response(code=200, description="Product deleted successfully.")
    @products.response(code=404, description="Product not found.")
    @products.response(code=500, description="Error in server occurred.")
    def delete(self, product_id: int):
        """
        Endpoint to delete a product.
        """
        # Verifica se o produto existe
        product = self.product_repository.find_product_by_id(product_id=product_id)
        if not product:
            return {"error": "Product not found."}, 404

        try:
            # Diretório do produto no servidor
            product_folder = os.path.join(PRODUCT_UPLOAD_PATH, str(product_id))

            # Deleta o produto do banco de dados
            self.product_repository.delete_product(product=product)

            # Verifica se a pasta existe e a remove
            if os.path.exists(product_folder):
                shutil.rmtree(product_folder)  # Remove o diretório e todos os seus arquivos

            return {"message": "Product successfully deleted."}, 200

        except Exception as error:
            return {"error": str(error)}, 500
