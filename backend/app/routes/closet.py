from flask import Blueprint, jsonify, request
from app.model import Product, SeasonStyle, ProductSubscription
from app import db
from app.auth_utils import decode_token  # Utility function to decode tokens

closet_bp = Blueprint('closet', __name__)

def get_user_from_token():
    """Helper function to extract user_id from the Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, jsonify({"error": "Authorization token missing or invalid"})

    token = auth_header.split(" ")[1]  # Extract token from "Bearer <token>"
    try:
        user_id = decode_token(token)  # Assume `decode_token` returns the user_id from the token
        return user_id, None
    except Exception as e:
        return None, jsonify({"error": f"Invalid token: {str(e)}"})


@closet_bp.route('/api/user/products', methods=['GET'])
def get_user_products():
    user_id, error_response = get_user_from_token()
    if error_response:
        return error_response
    try:
        # Predefined product categories
        product_categories = ['shirt', 'pant', 'accessory', 'shoe', 'outerwear', 'dress']

        # Query all products the user is subscribed to
        products = (
            db.session.query(Product)
            .join(ProductSubscription, Product.ProductID == ProductSubscription.product_id)
            .filter(ProductSubscription.user_id == user_id)
            .all()
        )

        if not products:
            return jsonify({"error": "No products found for the user"}), 404

        result = []
        for product in products:
            product_dict = {c.name: getattr(product, c.name) for c in product.__table__.columns}

            category = None
            for cat in product_categories:
                if getattr(product, cat):
                    category = cat
                    break 

            product_dict['category'] = category

            if product.season_style:
                season_style_dict = {
                    c.name: getattr(product.season_style, c.name)
                    for c in product.season_style.__table__.columns
                    if c.name != 'ProductID'
                }
                product_dict["season_style"] = season_style_dict
            else:
                product_dict["season_style"] = None

            result.append(product_dict)

        return jsonify({"user_id": user_id, "products": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@closet_bp.route('/api/user/products/<int:product_id>', methods=['DELETE'])
def delete_user_product(product_id):
    user_id, error_response = get_user_from_token()
    if error_response:
        return error_response

    try:
        # Query to find the product subscription record between the user and the product
        subscription = (
            db.session.query(ProductSubscription)
            .filter_by(user_id=user_id, product_id=product_id)
            .first()
        )

        if not subscription:
            return jsonify({"error": "Subscription not found"}), 404

        # Remove the subscription without deleting the product itself
        db.session.delete(subscription)
        db.session.commit()

        return jsonify({"message": f"User {user_id} unsubscribed from product {product_id}"}), 200

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
    user_id, error_response = get_user_from_token()
    if error_response:
        return error_response

    try:
        # Get the payload from the request
        data = request.get_json()
        if not data or 'products' not in data:
            return jsonify({"error": "Invalid payload"}), 400

        # Extract the list of products from the payload
        products = data['products']

        if not isinstance(products, list):
            return jsonify({"error": "Products should be a list"}), 400

        added_products = []
        for product_data in products:
            product_id = product_data.get('ProductID')

            existing_subscription = (
                db.session.query(ProductSubscription)
                .filter_by(user_id=user_id, product_id=product_id)
                .first()
            )

            if existing_subscription:
                continue

            subscription = ProductSubscription(user_id=user_id, product_id=product_id)
            db.session.add(subscription)
            added_products.append(product_id)
        db.session.commit()

        return jsonify({
            "message": f"Successfully added {len(added_products)} products for user {user_id}",
            "added_products": added_products
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500