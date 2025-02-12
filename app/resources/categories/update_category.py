import unicodedata
from flask_restx import Resource
from app.repositories import CategoryRepository
from . import categories
from . args_categories import args_for_categories_endpoint as args_params


@categories.route("/update/<int:category_id>")
class UpdateCategory(Resource):
    category_repository = CategoryRepository()

    @categories.expect(args_params)
    @categories.response(code=200, description="Category updated successfully.")
    @categories.response(code=404, description="Category not found.")
    @categories.response(code=409, description="Category name conflict. The provided category name already exists in the database.")
    @categories.response(code=500, description="Error in server as occurred.")
    def put(self, category_id: int):
        """
        Endpoint to update an existing category by id.
        """
        data = args_params.parse_args()

        # Formata o nome para maiúsculas, similar à criação
        data['name'] = data['name'].upper()

        # Geração de 'url_name', como na criação
        url_name = "".join(c for c in unicodedata.normalize('NFD', data['name']) if unicodedata.category(c) != 'Mn')
        url_name = url_name.replace(' ', '_').replace(',', '')
        data['url_name'] = url_name

        # Verifica se o nome já existe em outra categoria
        category_by_name = self.category_repository.find_category_by_name(category_name=data['name'])
        if category_by_name and category_by_name.id != category_id:
            return {"error": f"The category name '{data['name']}' is registered in another category."}, 409

        # Verifica se a categoria com o 'category_id' existe
        category_found = self.category_repository.find_category_by_id(category_id=category_id)
        if not category_found:
            return {"error": f"Category '{category_id}' not registered."}, 404

        try:
            # Atualiza a categoria existente
            self.category_repository.update_category(category=category_found, **data)

            # Retorna a resposta JSON com os dados atualizados
            return self.category_repository.json(category=category_found), 200

        except Exception as error:
            return {"error": str(error)}, 500
