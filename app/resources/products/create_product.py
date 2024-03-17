"""
This file contains Flask-RESTx resources for "post" product-related operations.
"""
from flask_restx import Resource
from app.models.product import ProductModel
from app.repositories import ProductRepository

from . import products
from. args_products import args_for_products_endpoint as args_params


@products.route("/create/")
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

        product = ProductModel(**data)

        try:
            self.product_repository.add_product(product=product)
            return {"message": self.product_repository.json(product=product)}, 201
        except Exception as error:
            return {"error": error}, 500
