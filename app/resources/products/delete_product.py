"""
This file contains Flask-RESTx resources for "delete" product-related operations.
"""
from flask_restx import Resource
from app.repositories import ProductRepository

from . import products


@products.route("/delete/<int:product_id>/")
class DeleteProduct(Resource):
    product_repository = ProductRepository()

    @products.response(code=200, description="Product deleted successfully.")
    @products.response(code=404, description="Product not found.")
    @products.response(code=500, description="Error in server occurred.")
    def delete(self, product_id: int):
        """
        Endpoint to delete a product.
        """
        product = self.product_repository.find_product_by_id(product_id=product_id)
        if not product:
            return {"error": "Product not found."}, 404

        try:
            self.product_repository.delete_product(product=product)
            return {"message": "Product successfully deleted."}, 200
        except Exception as error:
            return {"error", error}, 500
