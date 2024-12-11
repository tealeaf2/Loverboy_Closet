# model.py
from . import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    # Outfits created by this user
    outfits = db.relationship('Outfit', back_populates='user', cascade='all, delete-orphan')

    # Outfits this user is subscribed to
    subscribed_outfits = db.relationship('OutfitSubscription', back_populates='user')

    # Products this user is subscribed to
    subscribed_products = db.relationship('ProductSubscription', back_populates='user')

class Outfit(db.Model):
    __tablename__ = 'outfits'
    outfit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # The creator (owner) of the outfit
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', back_populates='outfits')

    # Users subscribed to this outfit
    subscribers = db.relationship('OutfitSubscription', back_populates='outfit', cascade='all, delete-orphan')

    # Foreign keys for products that make up the outfit
    shirt_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=True)
    pant_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=True)
    accessory_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=True)
    shoe_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=True)
    outerwear_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=True)
    dress_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=True)

    # Direct relationships to product categories
    shirt = db.relationship('Product', foreign_keys=[shirt_id])
    pant = db.relationship('Product', foreign_keys=[pant_id])
    accessory = db.relationship('Product', foreign_keys=[accessory_id])
    shoe = db.relationship('Product', foreign_keys=[shoe_id])
    outerwear = db.relationship('Product', foreign_keys=[outerwear_id])
    dress = db.relationship('Product', foreign_keys=[dress_id])

    # Subscription count
    subscribe_count = db.Column(db.Integer, default=1, nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.Text, nullable=False)
    masterCategory = db.Column(db.Text, nullable=False)
    subCategory = db.Column(db.Text, nullable=False)
    articleType = db.Column(db.Text, nullable=False)
    baseColour = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    productDisplayName = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, default=0.0, nullable=False)
    favorite = db.Column(db.Boolean, default=False, nullable=False)

    # Category-specific relationships
    shirt = db.relationship('Shirt', back_populates='product', uselist=False)
    pant = db.relationship('Pant', back_populates='product', uselist=False)
    accessory = db.relationship('Accessory', back_populates='product', uselist=False)
    shoe = db.relationship('Shoe', back_populates='product', uselist=False)
    outerwear = db.relationship('Outerwear', back_populates='product', uselist=False)
    dress = db.relationship('Dress', back_populates='product', uselist=False)

    season_style = db.relationship('SeasonStyle', back_populates='product', uselist=False)

    # Users subscribed to this product
    subscribers = db.relationship('ProductSubscription', back_populates='product', cascade='all, delete-orphan')

class OutfitSubscription(db.Model):
    __tablename__ = 'outfit_subscriptions'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfits.outfit_id'), primary_key=True)

    user = db.relationship('User', back_populates='subscribed_outfits')
    outfit = db.relationship('Outfit', back_populates='subscribers')

class ProductSubscription(db.Model):
    __tablename__ = 'product_subscriptions'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)

    user = db.relationship('User', back_populates='subscribed_products')
    product = db.relationship('Product', back_populates='subscribers')

class Shirt(db.Model):
    __tablename__ = 'shirts'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)
    Material = db.Column(db.Text, default=None)
    product = db.relationship('Product', back_populates='shirt')

class Pant(db.Model):
    __tablename__ = 'pants'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)
    WaistLength = db.Column(db.Float, default=0)
    product = db.relationship('Product', back_populates='pant')

class Accessory(db.Model):
    __tablename__ = 'accessories'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)
    SizeinCM = db.Column(db.Float, default=0)
    product = db.relationship('Product', back_populates='accessory')

class Shoe(db.Model):
    __tablename__ = 'shoes'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)
    Comfort = db.Column(db.Text, default=None)
    product = db.relationship('Product', back_populates='shoe')

class Outerwear(db.Model):
    __tablename__ = 'outerwear'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)
    Thickness = db.Column(db.Text, default=None)
    product = db.relationship('Product', back_populates='outerwear')

class Dress(db.Model):
    __tablename__ = 'dresses'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)
    Design = db.Column(db.Text, default=None)
    product = db.relationship('Product', back_populates='dress')

class SeasonStyle(db.Model):
    __tablename__ = 'season_styles'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)

    Fall = db.Column(db.Boolean, default=False)
    Winter = db.Column(db.Boolean, default=False)
    Spring = db.Column(db.Boolean, default=False)
    Summer = db.Column(db.Boolean, default=False)

    Casual = db.Column(db.Boolean, default=False)
    Business = db.Column(db.Boolean, default=False)
    Sport = db.Column(db.Boolean, default=False)

    product = db.relationship('Product', back_populates='season_style')
