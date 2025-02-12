"""
Este arquivo contém recursos Flask-RESTx para operações relacionadas à venda de produtos.
"""
from flask_restx import Resource
from app.models.sold_product import SoldProductModel
from app.repositories import SoldProductRepository, ProductRepository
from datetime import datetime

from . import sold_products
from .args_sold_product import args_for_sell_product_endpoint as args_params


@sold_products.route("/sell")
class SellProduct(Resource):
    sold_product_repository = SoldProductRepository()
    product_repository = ProductRepository()

    @sold_products.expect(args_params)
    @sold_products.response(code=201, description="Produto vendido com sucesso.")
    @sold_products.response(code=400, description="Dados inválidos fornecidos.")
    @sold_products.response(code=404, description="Produto não encontrado.")
    @sold_products.response(code=500, description="Ocorreu um erro no servidor.")
    def post(self):
        """
        Endpoint para vender um produto.
        """
        data = args_params.parse_args()

        product_id = data.get('product_id')
        quantity_sold = data.get('quantity_sold', 1)
        sale_price = data.get('sale_price')

        sale_date_str = data.get('sale_date')
        try:
            sale_date = datetime.fromisoformat(sale_date_str) if sale_date_str else datetime.now()
        except ValueError:
            return {"error": "Formato de data inválido. Use o formato ISO: YYYY-MM-DDTHH:MM."}, 400

        # Verifica se o produto existe
        product = self.product_repository.find_product_by_id(product_id=product_id)
        if not product:
            return {"error": "Produto não encontrado."}, 404

        # Verifica se há estoque suficiente (se aplicável)
        if hasattr(product, 'stock_quantity'):
            if product.stock_quantity < quantity_sold:
                return {"error": "Estoque insuficiente para o produto."}, 400
            product.stock_quantity -= quantity_sold
            self.product_repository.update_product(product=product)

        # Cria a instância do produto vendido
        sold_product = SoldProductModel(
            product_id=product_id,
            quantity_sold=quantity_sold,
            sale_price=sale_price,
            sale_date=sale_date
        )

        try:
            self.sold_product_repository.add_sold_product(sold_product=sold_product)
            return self.sold_product_repository.json(sold_product=sold_product), 201
        except Exception as error:
            return {"error": str(error)}, 500
