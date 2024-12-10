from flask import Blueprint, jsonify
from app.model import Product, SeasonStyle, ProductSubscription
from app import db

closet_bp = Blueprint('closet', __name__)

@closet_bp.route('/api/user/<int:user_id>/products', methods=['GET'])
def get_user_products(user_id):
    try:
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
