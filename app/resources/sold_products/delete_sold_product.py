from flask_restx import Resource
from app.repositories import SoldProductRepository
from . import sold_products


@sold_products.route("/delete/<int:sold_product_id>/")
class DeleteSoldProduct(Resource):
    sold_product_repository = SoldProductRepository()

    @sold_products.response(code=200, description="Produto vendido excluído com sucesso.")
    @sold_products.response(code=404, description="Produto vendido não encontrado.")
    @sold_products.response(code=500, description="Ocorreu um erro no servidor.")
    def delete(self, sold_product_id: int):
        """
        Endpoint para deletar um produto vendido.
        """
        sold_product = self.sold_product_repository.find_sold_product_by_id(sold_product_id=sold_product_id)
        if not sold_product:
            return {"error": "Produto vendido não encontrado."}, 404

        try:
            self.sold_product_repository.delete_sold_product(sold_product=sold_product)
            return {"message": "Produto vendido excluído com sucesso."}, 200
        except Exception as error:
            return {"error": str(error)}, 500
