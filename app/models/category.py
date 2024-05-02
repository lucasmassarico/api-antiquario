"""
This module defines the SQLAlchemy model class 'CategoryModel' representing product data,
including its unique identifier and name.
"""

from app import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    discount = db.Column(db.Float, default=0)

    def __repr__(self) -> str:
        self.name
