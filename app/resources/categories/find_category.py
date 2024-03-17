"""
This file contains Flask-RESTx resources for "get" product-related operations.
"""
from flask_restx import Resource


from app.repositories import CategoryRepository
from . import categories


@categories.route("/find/by_id/<int:category_id>")
class FindCategoryById(Resource):
    category_repository = CategoryRepository()

    @categories.response(code=200, description="Category successfully found.")
    @categories.response(code=404, description="Category not found.")
    def get(self, category_id: int):
        """
        Endpoint to find a category by their ID.
        """
        category = self.category_repository.find_category_by_id(category_id=category_id)
        if category:
            return {"category": self.category_repository.json(category=category)}
        return {"error": "Category not found."}, 404


@categories.route("/find/by_name/<string:category_name>")
class FindCategoryByName(Resource):
    category_repository = CategoryRepository()

    @categories.response(code=200, description="Category successfully found.")
    @categories.response(code=404, description="Category not found.")
    def get(self, category_name: str):
        """
        Endpoint to find a category by their name.
        """
        category_name = category_name.upper()

        category = self.category_repository.find_category_by_name(category_name=category_name)

        if category:
            return {"category": self.category_repository.json(category=category)}, 200

        return {"error": "Category not found."}, 404


@categories.route("/find/all/")
class FindAllCategories(Resource):
    category_repository = CategoryRepository()

    @categories.response(code=200, description="Categories successfully found.")
    @categories.response(code=404, description="Categories not found.")
    @categories.response(code=500, description="Error in server as occurred.")
    def get(self):
        """
        Endpoint to find all categories.
        """
        try:
            categories_type = self.category_repository.find_all_categories()
        except Exception as error:
            return {"error": error}, 500

        categories_to_json = []

        for category in categories_type:
            categories_to_json.append(self.category_repository.json(category=category))

        return {"categories": categories_to_json}, 200
