# category.py

"""
This module defines the SQLAlchemy model class `CategoryModel` representing category data,
including its unique identifier, name, URL-friendly name, and discount.
"""

from app import db


class CategoryModel(db.Model):
    """
    Represents a category in the application.

    Attributes:
        id (int): Primary key, unique identifier of the category.
        name (str): Name of the category.
        url_name (str): URL-friendly version of the category name.
        discount (float): Discount percentage applied to the category.
    """

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    url_name = db.Column(db.String(150), nullable=False)
    discount = db.Column(db.Float, default=0)

    def __repr__(self) -> str:
        """
        Returns a string representation of the category.

        Returns:
            str: The name of the category.
        """
        return f"{self.name}"
