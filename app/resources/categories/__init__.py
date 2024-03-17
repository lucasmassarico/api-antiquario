"""
File defining a Flask-RESTx Namespace for Categories CRUD operations.
"""
from flask_restx import Namespace

categories = Namespace(name="Categories", description="Categories CRUD")

from . create_category import CreateCategory
from . find_category import FindCategoryById, FindCategoryByName, FindAllCategories
from . update_category import UpdateCategory
from . delete_category import DeleteProduct
