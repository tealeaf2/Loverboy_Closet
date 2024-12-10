# model.py
from . import db
from sqlalchemy.sql import func

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.Text)
    masterCategory = db.Column(db.Text)
    subCategory = db.Column(db.Text)
    articleType = db.Column(db.Text)
    baseColour = db.Column(db.Text)
    # season = db.Column(db.Text)
    year = db.Column(db.Integer)
    usage = db.Column(db.Text)
    productDisplayName = db.Column(db.Text)
    image_url = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    favorite = db.Column(db.Boolean, default=False)

    # Relationships to category-specific tables
    shirt = db.relationship('Shirt', back_populates='product', uselist=False)
    pant = db.relationship('Pant', back_populates='product', uselist=False)
    accessory = db.relationship('Accessory', back_populates='product', uselist=False)
    shoe = db.relationship('Shoe', back_populates='product', uselist=False)
    outerwear = db.relationship('Outerwear', back_populates='product', uselist=False)
    dress = db.relationship('Dress', back_populates='product', uselist=False)

    season_style = db.relationship('SeasonStyle', back_populates='product', uselist=False)

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


# New model for seasons and style
class SeasonStyle(db.Model):
    __tablename__ = 'season_styles'
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), primary_key=True)

    # Seasons
    Fall = db.Column(db.Boolean, default=False)
    Winter = db.Column(db.Boolean, default=False)
    Spring = db.Column(db.Boolean, default=False)
    Summer = db.Column(db.Boolean, default=False)

    # Styles
    Casual = db.Column(db.Boolean, default=False)
    Business = db.Column(db.Boolean, default=False)
    Sport = db.Column(db.Boolean, default=False)

    product = db.relationship('Product', back_populates='season_style')
