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
        product_image = self.product_image_repository.find_product_image_by_id(product_image_id=id_product_image)
        if not product_image:
            return {"error": "Product image not exists"}, 400
