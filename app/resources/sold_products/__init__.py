from flask_restx import Namespace


sold_products = Namespace(name="Sold Products", description="Sold Products CRUD")

from .sell_products import SellProduct
from .find_sold_products import FindAllSoldProducts, FindSoldProductById
from .delete_sold_product import DeleteSoldProduct
