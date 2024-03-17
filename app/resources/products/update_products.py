"""
This file contains Flask-RESTx resources for "put" products-related operations.
"""
from flask_restx import Resource
from app.repositories import ProductRepository
from . import products
from . args_products import args_for_products_endpoint as args_params


@products.route("/update/<int:product_id>/")
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
        if product_by_name:
            if product_by_name.id != product_id:
                return {"error": f"The name '{data['name']}' are registered in another product."}, 409

        errors = self.product_repository.check_category_existence(category_id=data['id_category'])
        if errors:
            return {"errors": errors}, 400

        product_found = self.product_repository.find_product_by_id(product_id=product_id)

        if product_found:
            try:
                # gambiarra, deveria fazer uma func.
                if not data['description']:
                    data['description'] = product_found.description

                if not data['price']:
                    data['price'] = product_found.price

                if not data['stock_quantity']:
                    data['stock_quantity'] = product_found.stock_quantity

                if not data['activated']:
                    data['activated'] = product_found.activated

                self.product_repository.update_product(product=product_found, **data)
                return self.product_repository.json(product=product_found), 200

            except Exception as error:
                return {"error": error}, 500

        return {"error": f"Product '{product_id}' not registered."}, 404
