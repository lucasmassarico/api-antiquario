from app import db
from datetime import datetime


class SoldProductModel(db.Model):
    __tablename__ = "sold_products"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete="CASCADE"),
        nullable=True
    )
    quantity_sold = db.Column(db.Integer, default=1, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    product = db.relationship('ProductModel', backref=db.backref('sales', lazy=True))

    def __repr__(self):
        return f"<SoldProduct id={self.id} product_id={self.product_id} quantity={self.quantity_sold}>"
