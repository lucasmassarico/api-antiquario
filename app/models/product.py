"""
This module defines the SQLAlchemy model class 'ProductModel' representing product data,
including its unique identifier, name, description, price and others.
"""

from app import db
from datetime import datetime


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True, unique=True)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    stock_quantity = db.Column(db.Integer, default=1)
    activated = db.Column(db.Boolean(), default=True)
    image_thumbnail_name = db.Column(db.Text)
    publication_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return self.name


class ProductImagesModel(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    image_path = db.Column(db.Text)
