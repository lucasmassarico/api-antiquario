from flask_restx import Resource
from . import imagens_for_products
from app.repositories import ProductRepository, ProductImagesRepository


@imagens_for_products.route("/find/by_product_id/<int:product_id>")
class FindProductImage(Resource):
    product_repository = ProductRepository()
    product_images_repository = ProductImagesRepository()

    def get(self, product_id: int):
        """
        Endpoint to find paths of images product
        """
        product = self.product_repository.find_product_by_id(product_id=product_id)
        if not product:
            return {"error": "Product not found."}, 404

        images_paths = self.product_images_repository.find_product_image_by_product_id(product_id=product_id)
        if not images_paths:
            return {"message": "No Images registered in product."}, 200

        image_paths_list = [{"id": image.id, "image_path": image.image_path} for image in images_paths]

        return image_paths_list, 200
