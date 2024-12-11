from flask import Blueprint, jsonify
from app.model import Product, SeasonStyle, UserProductOutfit
from app import db

user = 20

closet_bp = Blueprint('closet', __name__)
@closet_bp.route('/api/user/<int:user_id>/products', methods=['GET'])
def get_user_products(user_id):
  try:
    # Query all products for the user
    products = (
        db.session.query(Product)
        .join(UserProductOutfit, Product.ProductID == UserProductOutfit.product_id)
        .filter(UserProductOutfit.user_id == user_id)
        .all()
    )
      
    if not products:
      return jsonify({"error": "No products found for the user"}), 404

    # Build the response data dynamically
    result = []
    for product in products:
        # Convert product attributes to a dictionary
        product_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}

        # Include related SeasonStyle data if it exists
        if product.season_style:
            season_style_dict = {
                c.name: getattr(product.season_style, c.name)
                for c in product.season_style.__table__.columns
                if c.name != 'ProductID'  # Exclude foreign key
            }
            product_dict["season_style"] = season_style_dict
        else:
            product_dict["season_style"] = None

        result.append(product_dict)

    return jsonify({"user_id": user_id, "products": result}), 200

  except Exception as e:
      return jsonify({"error": str(e)}), 500
  

@closet_bp.route('/api/user/<int:user_id>/products/<int:product_id>', methods=['DELETE'])
def delete_user_product(user_id, product_id):
    try:
        # Query to find the association between the user and the product
        user_product_outfit = (
            db.session.query(UserProductOutfit)
            .filter_by(user_id=user_id, product_id=product_id)
            .first()
        )

        if not user_product_outfit:
            return jsonify({"error": "Association not found"}), 404

        # Remove the association without deleting the product itself
        db.session.delete(user_product_outfit)
        db.session.commit()

        return jsonify({"message": f"Product {product_id} removed from user {user_id}"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@closet_bp.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        # Query all products from the database
        products = Product.query.all()

        if not products:
            return jsonify({"error": "No products found"}), 404

        # Build the response data dynamically
        product_list = []
        for product in products:
            # Convert product attributes to a dictionary
            product_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}

            # Include related SeasonStyle data if it exists
            if product.season_style:
                season_style_dict = {
                    c.name: getattr(product.season_style, c.name)
                    for c in product.season_style.__table__.columns
                    if c.name != 'ProductID'  # Exclude foreign key
                }
                product_dict["season_style"] = season_style_dict
            else:
                product_dict["season_style"] = None

            product_list.append(product_dict)

        # Return the products as JSON
        return jsonify({"success": True, "products": product_list}), 200

    except Exception as e:
        # Handle errors gracefully
        return jsonify({"success": False, "error": str(e)}), 500

@closet_bp.route('/api/products', methods=['POST']) 
def add_products_user():
    user = 20

    