"""
This module provides a repository class to interact with the database and perform operations related to all models management.
"""
from app import db
from app.models.product import ProductModel, ProductImagesModel
from app.models.category import CategoryModel
from sqlalchemy import not_, and_, or_
from typing import Union


class ProductRepository:
    """
    ProductRepository class for handling products-related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to product management.
    """
    @staticmethod
    def add_product(product: ProductModel):
        """
        Add a new product to the database.

        :param product: Product object representing the product to be added.
        :type product: ProductModel
        :return: None       :rtype:
        """
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def find_product_by_id(product_id: int) -> ProductModel:
        """
        Retrieve a product by their ID from the database.

        :param product_id: ID of the product to be retrieved.
        :type product_id: int
        :return: product object if found, else None.
        :rtype: ProductModel
        """
        return ProductModel.query.get(product_id)

    @staticmethod
    def find_products_by_category_id(category_id: int):
        products = ProductModel.query.filter_by(id_category=category_id).all()

        return products

    @staticmethod
    def find_products_by_name(product_name: str) -> ProductModel:
        return ProductModel.query.filter_by(name=product_name).first()

    @staticmethod
    def find_all_products(excluded_categories=None):
        """
        Retrieve all products from the database, excluding those in excluded_categories.
        """
        query = ProductModel.query

        if excluded_categories:
            query = query.filter(not_(ProductModel.id_category.in_(excluded_categories)))

        return query.all()

    @staticmethod
    def full_text_search(query, excluded_categories):
        products = db.session.query(ProductModel).filter(
            or_(
                ProductModel.name.ilike(f'%{query}%'),
                ProductModel.description.ilike(f'%{query}%')
            )
        )

        if excluded_categories:
            products = products.filter(
                not_(ProductModel.id_category.in_(excluded_categories))
            )

        return products.all()

    @staticmethod
    def update_product(product: ProductModel,
                       name: str,
                       id_category: int,
                       description: str,
                       price: float,
                       stock_quantity: int,
                       activated: bool,
                       image_thumbnail_name: str
                       ):
        product.name = name
        product.id_category = id_category
        product.description = description
        product.price = price
        product.stock_quantity = stock_quantity
        product.activated = activated
        product.image_thumbnail_name = image_thumbnail_name

        db.session.add(product)
        db.session.commit()

    @staticmethod
    def delete_product(product: ProductModel):
        """
        Delete a product in database.
        """
        db.session.delete(product)
        db.session.commit()

    @staticmethod
    def check_category_existence(category_id: int) -> Union[dict, None]:
        """
        Check if the provided category id are associated with existing category.
        """
        errors = dict()

        category = CategoryRepository.find_category_by_id(category_id=category_id)
        if not category:
            errors['id_category'] = f"ID '{category_id}' must be associated with an existing category."

        return errors or None

    @staticmethod
    def json(product: ProductModel) -> dict:
        return {
            "id": product.id,
            "name": product.name,
            "id_category": product.id_category,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "activated": product.activated,
            "image_thumbnail_name": product.image_thumbnail_name,
            "publication_date": str(product.publication_date.strftime("%d-%m-%Y %H:%M:%S"))
        }


class ProductImagesRepository:
    """
    ProductImagesRepository class for handling products images related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to product images management.
    """
    @staticmethod
    def add_product_image(product_image: ProductImagesModel):
        """
        Add a new product image path to the database.
        """
        db.session.add(product_image)
        db.session.commit()

    @staticmethod
    def find_product_image_by_product_id(product_id: int) -> [ProductImagesModel]:
        """
        Retrieve a product imagem by product ID from the database.
        """
        return ProductImagesModel.query.filter_by(id_product=product_id).all()

    @staticmethod
    def find_product_image_by_id(product_image_id: int):
        """
        Retrieve a product image by they id.
        """
        return ProductImagesModel.query.get(product_image_id)

    @staticmethod
    def find_all_products_image():
        """
        Retrieve all products images from the database.
        """
        return ProductImagesModel.query.all()

    @staticmethod
    def delete_product_image(product_image: ProductImagesModel):
        """
        Delete a product image in database.
        """
        db.session.delete(product_image)
        db.session.commit()

    @staticmethod
    def json(product_image: ProductImagesModel) -> dict:
        return {
            "id": product_image.id,
            "id_product": product_image.id_product,
            "image_path": product_image.image_path
        }


class CategoryRepository:
    """
    CategoryRepository class for handling category-related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to category management.
    """
    @staticmethod
    def add_category(category: CategoryModel):
        """
        Add a new category to the database.

        :param category: Product object representing the product to be added.
        :type category: CategoryModel
        :return: None       :rtype:
        """
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def find_category_by_id(category_id: int) -> CategoryModel:
        """
        Retrieve a product by their ID from the database.

        :param category_id: ID of the product to be retrieved.
        :type category_id: int
        :return: category object if found, else None.
        :rtype: CategoryModel
        """
        return CategoryModel.query.get(category_id)

    @staticmethod
    def find_category_by_name(category_name: str) -> CategoryModel:
        return CategoryModel.query.filter_by(name=category_name).first()

    @staticmethod
    def find_category_by_url_name(url_name: str) -> CategoryModel:
        return CategoryModel.query.filter_by(url_name=url_name).first()

    @staticmethod
    def find_all_categories():
        """
        Retrive all categories from the database.
        """
        return CategoryModel.query.all()

    @staticmethod
    def update_category(category: CategoryModel, name: str):
        category.name = name

        db.session.add(category)
        db.session.commit()

    @staticmethod
    def delete_category(category: CategoryModel):
        """
        Delete a product in database.
        """
        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def json(category: CategoryModel) -> dict:
        return {
            "id": category.id,
            "name": category.name,
            "url_name": category.url_name,
            "discount": category.discount
        }
