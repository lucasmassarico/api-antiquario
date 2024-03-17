"""
This file contains Flask-RESTx resources for "post" category-related operations.
"""
from flask_restx import Resource
from app.models.category import CategoryModel
from app.repositories import CategoryRepository

from . import categories
from . args_categories import args_for_categories_endpoint as args_params


@categories.route("/create/")
class CreateCategory(Resource):
    category_repository = CategoryRepository()

    @categories.expect(args_params)
    @categories.response(code=201, description="Category created successfully.")
    @categories.response(code=409, description="Category name conflict. The provided category name already exists in the database.")
    @categories.response(code=500, description="Error in server as occurred.")
    def post(self):
        """
        Endpoint to create a new category.
        """
        data = args_params.parse_args()
        data['name'] = data['name'].upper()

        if self.category_repository.find_category_by_name(category_name=data['name']):
            return {"error": f"The category name '{data['name']}' already exists in database."}, 409

        category = CategoryModel(**data)

        try:
            self.category_repository.add_category(category=category)
            return {"message": self.category_repository.json(category=category)}, 201
        except Exception as error:
            return {"error": error}, 500
