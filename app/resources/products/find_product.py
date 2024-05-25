"""
This file contains Flask-RESTx resources for "get" product-related operations.
"""
from flask_restx import Resource

from app.repositories import ProductRepository, CategoryRepository
from . import products


@products.route("/find/by_id/<int:product_id>/")
class FindProductById(Resource):
    product_repository = ProductRepository()

    @products.response(code=200, description="product successfully found.")
    @products.response(code=404, description="product not found.")
    def get(self, product_id: int):
        """
        Endpoint to find a product by their ID.
        """
        product = self.product_repository.find_product_by_id(product_id=product_id)
        if product:
            return self.product_repository.json(product=product), 200
        return {"error": "Product not found."}, 404


@products.route("/find/by_name/<string:product_name>/")
class FindProductByName(Resource):
    product_repository = ProductRepository()

    @products.response(code=200, description="Product successfully found.")
    @products.response(code=404, description="Product not found.")
    def get(self, product_name: str):
        """
        Endpoint to find a product by their name.
        """
        product_name = product_name.upper()

        product = self.product_repository.find_products_by_name(product_name=product_name)

        if product:
            return self.product_repository.json(product=product), 200
        return {"error": "Product not found."}, 404


@products.route("/find/all/")
class FindAllProducts(Resource):
    product_repository = ProductRepository()

    @products.response(code=200, description="Products successfully found.")
    @products.response(code=404, description="Products not found.")
    @products.response(code=500, description="Error in server as occurred.")
    def get(self):
        """
        Endpoint to find all products.
        """
        try:
            products_types = self.product_repository.find_all_products()
        except Exception as error:
            return {"error": error}, 500

        products_to_json = []

        for product in products_types:
            products_to_json.append(self.product_repository.json(product=product))

        return products_to_json, 200


@products.route("/find/by_category_id/<int:category_id>")
class FindProductsByCategoryId(Resource):
    product_repository = ProductRepository()
    category_repository = CategoryRepository

    @products.response(code=200, description="Products successfully found.")
    @products.response(code=400, description="The provided category IDis not associated with any existing category.")
    @products.response(code=404, description="Products not found.")
    @products.response(code=500, description="Error in server as occurred.")
    def get(self, category_id: int):
        # check if category exists

        if not self.category_repository.find_category_by_id(category_id=category_id):
            return {"error": f"Category ID '{category_id}' not exists."}, 400

        try:
            products_type = self.product_repository.find_products_by_category_id(category_id=category_id)

        except Exception as error:
            return {"error": error}, 500

        products_to_json = []

        for product in products_type:
            products_to_json.append(self.product_repository.json(product=product))

        return products_to_json, 200
