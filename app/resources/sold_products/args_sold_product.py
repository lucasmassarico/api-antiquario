from flask_restx import reqparse


args_for_sell_product_endpoint = reqparse.RequestParser()
args_for_sell_product_endpoint.add_argument('product_id', type=int, required=True, help='ID do produto a ser vendido.')
args_for_sell_product_endpoint.add_argument('quantity_sold', type=int, required=False, default=1, help='Quantidade vendida do produto.')
args_for_sell_product_endpoint.add_argument('sale_price', type=float, required=True, help='Preço de venda do produto.')
args_for_sell_product_endpoint.add_argument('sale_date', type=str, required=False, help='Data da venda.')

args_for_find_sold_products_endpoint = reqparse.RequestParser()
args_for_find_sold_products_endpoint.add_argument('start_date', type=str, required=False, help='Data de início para filtrar vendas.')
args_for_find_sold_products_endpoint.add_argument('end_date', type=str, required=False, help='Data de fim para filtrar vendas.')
args_for_find_sold_products_endpoint.add_argument('product_id', type=int, required=False, help='Filtrar vendas por ID do produto.')
