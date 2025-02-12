# repositories/__init__.py

"""
This module provides repository classes to interact with the database and perform operations related to the management of products, product images, categories, and users.
"""

from typing import Union, List

from sqlalchemy import not_, or_
from werkzeug.security import generate_password_hash

from app import db
from app.models.category import CategoryModel
from app.models.product import ProductModel, ProductImagesModel
from app.models.user import UserModel
from app.models.sold_product import SoldProductModel


class ProductRepository:
    """
    A repository class for handling product-related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to product management.
    """

    @staticmethod
    def add_product(product: ProductModel) -> None:
        """
        Adds a new product to the database.

        Args:
            product (ProductModel): The product to be added.
        """
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def find_product_by_id(product_id: int) -> Union[ProductModel, None]:
        """
        Retrieves a product by its ID from the database.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            ProductModel or None: The product object if found, else None.
        """
        return ProductModel.query.get(product_id)

    @staticmethod
    def find_products_by_category_id(category_id: int) -> List[ProductModel]:
        """
        Retrieves all products belonging to a specific category.

        Args:
            category_id (int): The ID of the category.

        Returns:
            List[ProductModel]: A list of products in the specified category.
        """
        return ProductModel.query.filter_by(id_category=category_id).all()

    @staticmethod
    def find_products_by_name(product_name: str) -> Union[ProductModel, None]:
        """
        Retrieves a product by its name.

        Args:
            product_name (str): The name of the product.

        Returns:
            ProductModel or None: The product object if found, else None.
        """
        return ProductModel.query.filter_by(name=product_name).first()

    @staticmethod
    def find_all_products(excluded_categories: List[int] = None) -> List[ProductModel]:
        """
        Retrieves all products from the database, excluding those in specified categories.

        Args:
            excluded_categories (List[int], optional): A list of category IDs to exclude. Defaults to None.

        Returns:
            List[ProductModel]: A list of products.
        """
        query = ProductModel.query
        if excluded_categories:
            query = query.filter(not_(ProductModel.id_category.in_(excluded_categories)))
        return query.all()

    @staticmethod
    def full_text_search(query_str: str, excluded_categories: List[int] = None) -> List[ProductModel]:
        """
        Performs a full-text search on products based on a query string.

        Args:
            query_str (str): The search string.
            excluded_categories (List[int], optional): A list of category IDs to exclude. Defaults to None.

        Returns:
            List[ProductModel]: A list of products matching the search criteria.
        """
        products = db.session.query(ProductModel).filter(
            or_(
                ProductModel.name.ilike(f'%{query_str}%'),
                ProductModel.description.ilike(f'%{query_str}%')
            )
        )
        if excluded_categories:
            products = products.filter(
                not_(ProductModel.id_category.in_(excluded_categories))
            )
        return products.all()

    @staticmethod
    def update_product(
            product: ProductModel,
            name: str = None,
            id_category: int = None,
            description: str = None,
            price: float = None,
            stock_quantity: int = None,
            activated: bool = None,
            image_thumbnail_name: str = None
    ) -> None:
        """
        Updates an existing product in the database with only the provided fields.

        Args:
            product (ProductModel): The product to update.
            name (str, optional): The new name of the product.
            id_category (int, optional): The new category ID.
            description (str, optional): The new description.
            price (float, optional): The new price.
            stock_quantity (int, optional): The new stock quantity.
            activated (bool, optional): The new activation status.
            image_thumbnail_name (str, optional): The new thumbnail image name.
        """
        if name is not None:
            product.name = name
        if id_category is not None:
            product.id_category = id_category
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock_quantity is not None:
            product.stock_quantity = stock_quantity
        if activated is not None:
            product.activated = activated
        if image_thumbnail_name is not None:
            product.image_thumbnail_name = image_thumbnail_name

        db.session.add(product)
        db.session.commit()

    @staticmethod
    def delete_product(product: ProductModel) -> None:
        """
        Deletes a product from the database.

        Args:
            product (ProductModel): The product to delete.
        """
        db.session.delete(product)
        db.session.commit()

    @staticmethod
    def check_category_existence(category_id: int) -> Union[dict, None]:
        """
        Checks if a category exists for the given category ID.

        Args:
            category_id (int): The category ID to check.

        Returns:
            dict or None: A dictionary containing an error message if the category does not exist, else None.
        """
        errors = {}
        category = CategoryRepository.find_category_by_id(category_id=category_id)
        if not category:
            errors['id_category'] = f"ID '{category_id}' must be associated with an existing category."
        return errors or None

    @staticmethod
    def json(product: ProductModel) -> dict:
        """
        Serializes a product object to a JSON-compatible dictionary.

        Args:
            product (ProductModel): The product to serialize.

        Returns:
            dict: The serialized product data.
        """
        return {
            "id": product.id,
            "name": product.name,
            "id_category": product.id_category,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "activated": product.activated,
            "image_thumbnail_name": product.image_thumbnail_name,
            "publication_date": product.publication_date.strftime("%d-%m-%Y %H:%M:%S")
        }


class ProductImagesRepository:
    """
    A repository class for handling product image-related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to product image management.
    """

    @staticmethod
    def add_product_image(product_image: ProductImagesModel) -> None:
        """
        Adds a new product image path to the database.

        Args:
            product_image (ProductImagesModel): The product image to add.
        """
        db.session.add(product_image)
        db.session.commit()

    @staticmethod
    def find_product_image_by_product_id(product_id: int) -> List[ProductImagesModel]:
        """
        Retrieves all product images associated with a specific product ID.

        Args:
            product_id (int): The ID of the product.

        Returns:
            List[ProductImagesModel]: A list of product images.
        """
        return ProductImagesModel.query.filter_by(id_product=product_id).all()

    @staticmethod
    def find_product_image_by_id(product_image_id: int) -> Union[ProductImagesModel, None]:
        """
        Retrieves a product image by its ID.

        Args:
            product_image_id (int): The ID of the product image.

        Returns:
            ProductImagesModel or None: The product image if found, else None.
        """
        return ProductImagesModel.query.get(product_image_id)

    @staticmethod
    def find_all_products_image() -> List[ProductImagesModel]:
        """
        Retrieves all product images from the database.

        Returns:
            List[ProductImagesModel]: A list of all product images.
        """
        return ProductImagesModel.query.all()

    @staticmethod
    def delete_product_image(product_image: ProductImagesModel) -> None:
        """
        Deletes a product image from the database.

        Args:
            product_image (ProductImagesModel): The product image to delete.
        """
        db.session.delete(product_image)
        db.session.commit()

    @staticmethod
    def json(product_image: ProductImagesModel) -> dict:
        """
        Serializes a product image object to a JSON-compatible dictionary.

        Args:
            product_image (ProductImagesModel): The product image to serialize.

        Returns:
            dict: The serialized product image data.
        """
        return {
            "id": product_image.id,
            "id_product": product_image.id_product,
            "image_path": product_image.image_path
        }


class CategoryRepository:
    """
    A repository class for handling category-related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to category management.
    """

    @staticmethod
    def add_category(category: CategoryModel) -> None:
        """
        Adds a new category to the database.

        Args:
            category (CategoryModel): The category to add.
        """
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def find_category_by_id(category_id: int) -> Union[CategoryModel, None]:
        """
        Retrieves a category by its ID from the database.

        Args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            CategoryModel or None: The category object if found, else None.
        """
        return CategoryModel.query.get(category_id)

    @staticmethod
    def find_category_by_name(category_name: str) -> Union[CategoryModel, None]:
        """
        Retrieves a category by its name.

        Args:
            category_name (str): The name of the category.

        Returns:
            CategoryModel or None: The category object if found, else None.
        """
        return CategoryModel.query.filter_by(name=category_name).first()

    @staticmethod
    def find_category_by_url_name(url_name: str) -> Union[CategoryModel, None]:
        """
        Retrieves a category by its URL-friendly name.

        Args:
            url_name (str): The URL-friendly name of the category.

        Returns:
            CategoryModel or None: The category object if found, else None.
        """
        return CategoryModel.query.filter_by(url_name=url_name).first()

    @staticmethod
    def find_all_categories() -> List[CategoryModel]:
        """
        Retrieves all categories from the database.

        Returns:
            List[CategoryModel]: A list of all categories.
        """
        return CategoryModel.query.all()

    @staticmethod
    def update_category(category: CategoryModel, name: str, url_name: str, discount: float) -> None:
        """
        Updates an existing category in the database.

        Args:
            category (CategoryModel): The category to update.
            name (str): The new name of the category.
            url_name (str): The new URL-friendly name.
            discount (float): The new discount percentage.
        """
        category.name = name
        category.url_name = url_name
        category.discount = discount

        db.session.add(category)
        db.session.commit()

    @staticmethod
    def delete_category(category: CategoryModel) -> None:
        """
        Deletes a category from the database.

        Args:
            category (CategoryModel): The category to delete.
        """
        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def json(category: CategoryModel) -> dict:
        """
        Serializes a category object to a JSON-compatible dictionary.

        Args:
            category (CategoryModel): The category to serialize.

        Returns:
            dict: The serialized category data.
        """
        return {
            "id": category.id,
            "name": category.name,
            "url_name": category.url_name,
            "discount": category.discount
        }


class UserRepository:
    """
    A repository class for handling user-related database operations.

    This class encapsulates methods for interacting with the database to perform operations related to user management.
    """

    @staticmethod
    def add_user(user: UserModel) -> None:
        """
        Adds a new user to the database.

        Args:
            user (UserModel): The user to add.
        """
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def find_user_by_id(user_id: int) -> Union[UserModel, None]:
        """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserModel or None: The user object if found, else None.
        """
        return UserModel.query.get(user_id)

    @staticmethod
    def find_user_by_email(email: str) -> Union[UserModel, None]:
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            UserModel or None: The user object if found, else None.
        """
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def find_all_users() -> List[UserModel]:
        """
        Retrieves all users from the database.

        Returns:
            List[UserModel]: A list of all users.
        """
        return UserModel.query.all()

    @staticmethod
    def update_user(
        user: UserModel,
        name: str,
        email: str,
        password: str,
        active: bool,
        access_role: int
    ) -> None:
        """
        Updates the information of an existing user in the database.

        Args:
            user (UserModel): The user to update.
            name (str): The new name of the user.
            email (str): The new email address.
            password (str): The new password.
            active (bool): The new active status.
            access_role (int): The new access role.
        """
        user.name = name
        user.email = email
        user.password = generate_password_hash(password)
        user.active = active
        user.access_role = access_role

        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete_user(user: UserModel) -> None:
        """
        Deletes a user from the database.

        Args:
            user (UserModel): The user to delete.
        """
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def json(user: UserModel) -> dict:
        """
        Serializes a user object to a JSON-compatible dictionary.

        Args:
            user (UserModel): The user to serialize.

        Returns:
            dict: The serialized user data.
        """
        return {
            "id": user.id,
            "name": user.name.title(),
            "email": user.email.lower(),
            "active": user.active,
            "access_role": user.access_role,
        }


class SoldProductRepository:
    @staticmethod
    def add_sold_product(sold_product: SoldProductModel) -> None:
        """
        Adds a new product to the database.

        Args:
            sold_product (SoldProductModel): The product to be added.
        """
        db.session.add(sold_product)
        db.session.commit()

    @staticmethod
    def find_sold_product_by_id(sold_product_id: int) -> Union[SoldProductModel, None]:
        """
        Retrieves a product by its ID from the database.

        Args:
            sold_product_id (int): The ID of the product to retrieve.

        Returns:
            ProductModel or None: The product object if found, else None.
        """
        return SoldProductModel.query.get(sold_product_id)

    @staticmethod
    def find_all_products_sold() -> List[SoldProductModel]:
        """
        Retrieves all products from the database, excluding those in specified categories.

        Returns:
            List[SoldProductModel]: A list of products.
        """
        return SoldProductModel.query.all()

    @staticmethod
    def delete_sold_product(sold_product: SoldProductModel) -> None:
        """
        Deletes a product from the database.

        Args:
            sold_product (ProductModel): The product to delete.
        """
        db.session.delete(sold_product)
        db.session.commit()

    @staticmethod
    def json(sold_product: SoldProductModel) -> dict:
        """
        Serializes a product object to a JSON-compatible dictionary.

        Args:
            sold_product (SoldProductModel): The product to serialize.

        Returns:
            dict: The serialized product data.
        """
        return {
            "id": sold_product.id,
            "product_id": sold_product.product_id,
            "quantity_sold": sold_product.quantity_sold,
            "sale_price": sold_product.sale_price,
            "sale_date": str(sold_product.sale_date)
        }
