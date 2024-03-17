"""
This file contains Flask-RESTx resources for "put" categories-related operations.
"""
from flask_restx import Resource
from app.repositories import CategoryRepository
from . import categories
from . args_categories import args_for_categories_endpoint as args_params


@categories.route("/update/<int:category_id>/")
class UpdateCategory(Resource):
    category_repository = CategoryRepository()

    @categories.expect(args_params)
    @categories.response(code=200, description="Category updated successfully.")
    @categories.response(code=404, description="Category not found.")
    @categories.response(code=409, description="Category name conflict. The provided category name already exists in the database.")
    @categories.response(code=500, description="Error in server as occurred.")
    def put(self, category_id: int):
        """
        Endpoint to update an existing category by id.
        """
        data = args_params.parse_args()
        data['name'] = data['name'].upper()

        category_by_name = self.category_repository.find_category_by_name(category_name=data['name'])
        if category_by_name:
            if category_by_name.id != category_id:
                return {"error": f"The name '{data['name']}' are registered in another category."}, 409

        category_found = self.category_repository.find_category_by_id(category_id=category_id)

        if category_found:
            try:
                self.category_repository.update_category(category=category_found, **data)

                return self.category_repository.json(category=category_found), 200

            except Exception as error:
                return {"error": error}, 500

        return {"error": f"Category '{category_id}' not registered."}, 404
