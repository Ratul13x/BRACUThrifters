from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Seller(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Buyer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    provider_name = db.Column(db.String(500), nullable=False)
    provider_phone = db.Column(db.String(500), nullable=False)
    product_picture = db.Column(db.String(1000), nullable=True) #image add
    stock = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)  # Reference to Seller model
    seller = db.relationship('Seller', backref=db.backref('products', lazy=True))  # Define the relationship to Seller
    

from datetime import datetime  # Import the datetime module directly

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    # order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Correct usage

    # Relationships
    buyer = db.relationship('Buyer', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))