"""
This file contains Flask-RESTx resources for "delete" category-related operations.
"""
from flask_restx import Resource
from app.repositories import CategoryRepository

from . import categories


@categories.route("/delete/<int:category_id>/")
class DeleteProduct(Resource):
    category_repository = CategoryRepository()

    @categories.response(code=200, description="Category deleted successfully.")
    @categories.response(code=404, description="Category not found.")
    @categories.response(code=500, description="Error in server occurred.")
    def delete(self, category_id: int):
        """
        Endpoint to delete a Category.
        """
        category = self.category_repository.find_category_by_id(category_id=category_id)
        if not category:
            return {"error": "Category not found."}, 404

        try:
            self.category_repository.delete_category(category=category)
            return {"message": "Category successfully deleted."}, 200
        except Exception as error:
            return {"error", error}, 500
