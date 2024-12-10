from flask import Blueprint, jsonify
from app import db
from ..model import Product, SeasonStyle

home_bp = Blueprint('home', __name__)

@home_bp.route('/product/12418', methods=['GET'])
def get_product_12418():
    # Query the product with ProductID = 12418
    product = Product.query.filter_by(ProductID=12418).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Convert product attributes to a dict
    product_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}

    # If there's a related SeasonStyle record, include it
    if product.season_style:
        season_style_dict = {c.name: getattr(product.season_style, c.name) 
                             for c in product.season_style.__table__.columns 
                             if c.name != 'ProductID'}
        product_dict["season_style"] = season_style_dict
    else:
        product_dict["season_style"] = None

    # Return the product info as JSON
    return jsonify(product_dict), 200