from sqlalchemy_data_model_visualizer import generate_data_model_diagram, add_web_font_and_interactivity
from app.models.user import UserModel
from app.models.sold_product import SoldProductModel
from app.models.product import ProductModel, ProductImagesModel
from app.models.category import CategoryModel


models = [UserModel, SoldProductModel, ProductModel, ProductImagesModel, CategoryModel]
output_file_name = 'my_data_model_diagram'
generate_data_model_diagram(models, output_file_name)
