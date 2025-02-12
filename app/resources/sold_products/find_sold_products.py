from flask_restx import Resource
from app.repositories import SoldProductRepository
from .args_sold_product import args_for_find_sold_products_endpoint as args_params
from . import sold_products


@sold_products.route("/find/by_id/<int:sold_product_id>/")
class FindSoldProductById(Resource):
    sold_product_repository = SoldProductRepository()

    @sold_products.response(code=200, description="Produto vendido encontrado com sucesso.")
    @sold_products.response(code=404, description="Produto vendido não encontrado.")
    def get(self, sold_product_id: int):
        """
        Endpoint para encontrar um produto vendido pelo seu ID.
        """
        sold_product = self.sold_product_repository.find_sold_product_by_id(sold_product_id=sold_product_id)
        if sold_product:
            return self.sold_product_repository.json(sold_product=sold_product), 200
        return {"error": "Produto vendido não encontrado."}, 404


@sold_products.route("/find/all/")
class FindAllSoldProducts(Resource):
    sold_product_repository = SoldProductRepository()

    @sold_products.response(code=200, description="Produtos vendidos encontrados com sucesso.")
    @sold_products.response(code=500, description="Ocorreu um erro no servidor.")
    def get(self):
        """
        Endpoint para encontrar todos os produtos vendidos.
        """
        try:
            sold_products_list = self.sold_product_repository.find_all_products_sold()

            sold_products_json = [
                self.sold_product_repository.json(sold_product=sp) for sp in sold_products_list
            ]

            return sold_products_json, 200
        except Exception as error:
            return {"error": str(error)}, 500
