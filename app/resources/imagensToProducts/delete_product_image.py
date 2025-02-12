import os
from flask_restx import Resource
from app.repositories import ProductImagesRepository

from . import imagens_for_products


@imagens_for_products.route("/delete/<int:id_product_image>")
class DeleteProductImage(Resource):
    product_image_repository = ProductImagesRepository()

    def delete(self, id_product_image: int):
        """
        Endpoint to delete a product image
        """
        # Procura a imagem pelo ID
        product_image = self.product_image_repository.find_product_image_by_id(product_image_id=id_product_image)
        if not product_image:
            return {"error": "Product image not exists"}, 404

        # Obtém o caminho relativo da imagem
        relative_image_path = product_image.image_path

        # Constrói o caminho absoluto da imagem de forma correta
        absolute_image_path = os.path.join("app/static/", relative_image_path)

        # Verifica se o arquivo existe no sistema de arquivos e tenta remover
        if os.path.exists(absolute_image_path):
            try:
                # Remove a imagem do sistema de arquivos
                print(f"Removing file: {absolute_image_path}")
                os.remove(absolute_image_path)
            except Exception as e:
                return {"error": f"Failed to remove image from server: {str(e)}"}, 500
        else:
            return {"error": f"File does not exist: {absolute_image_path}"}, 404

        try:
            # Remove a imagem do banco de dados
            self.product_image_repository.delete_product_image(product_image=product_image)
            return {"message": "Product image successfully deleted."}, 200
        except Exception as e:
            return {"error": f"Failed to delete product image: {str(e)}"}, 500
