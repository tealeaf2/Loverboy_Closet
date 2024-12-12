from flask import Blueprint, jsonify, request
from app.model import Outfit, Product, OutfitSubscription, ProductSubscription
from app import db

outfits_bp = Blueprint('outfits', __name__)

@outfits_bp.route('/api/outfits/<int:outfit_id>', methods=['DELETE'])
def delete_outfit(outfit_id):
    try:
        outfit = Outfit.query.get(outfit_id)
        if not outfit:
            return jsonify({'error': 'Outfit not found'}), 404

        db.session.delete(outfit)
        db.session.commit()

        return jsonify({'message': 'Outfit and associated subscriptions deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@outfits_bp.route('/api/user/<int:user_id>/outfits', methods=['GET'])
def get_user_outfits(user_id):
    user_id = 20
    try:
        outfits = db.session.query(Outfit).filter_by(user_id=user_id).all()

        if not outfits:
            return jsonify({"error": f"No outfits found for user {user_id}"}), 404

        result = []
        for outfit in outfits:
            # Collect product references from the outfit
            product_categories = ['shirt', 'pant', 'accessory', 'shoe', 'outerwear', 'dress']
            products_info = []
            true_tags = set()  # Collect tags that are True across all products
            total_price = 0  # Initialize total price for the outfit

            for category in product_categories:
                product_obj = getattr(outfit, category)
                if product_obj:
                    # Add the product's price to the total price
                    total_price += product_obj.price

                    # Include all season styles (True and False)
                    season_style_dict = (
                        {
                            "Fall": product_obj.season_style.Fall,
                            "Winter": product_obj.season_style.Winter,
                            "Spring": product_obj.season_style.Spring,
                            "Summer": product_obj.season_style.Summer,
                            "Casual": product_obj.season_style.Casual,
                            "Business": product_obj.season_style.Business,
                            "Sport": product_obj.season_style.Sport
                        }
                        if product_obj.season_style
                        else None
                    )

                    # Collect only True tags for this product
                    if season_style_dict:
                        true_tags.update(
                            [key for key, value in season_style_dict.items() if value]
                        )

                    product_dict = {
                        "ProductID": product_obj.ProductID,
                        "gender": product_obj.gender,
                        "masterCategory": product_obj.masterCategory,
                        "subCategory": product_obj.subCategory,
                        "articleType": product_obj.articleType,
                        "baseColour": product_obj.baseColour,
                        "year": product_obj.year,
                        "usage": product_obj.usage,
                        "productDisplayName": product_obj.productDisplayName,
                        "image_url": product_obj.image_url,
                        "price": product_obj.price,
                        "favorite": product_obj.favorite,
                        "category": category,
                        "season_style": season_style_dict  # Include all tags
                    }

                    products_info.append(product_dict)

            outfit_data = {
                "outfit_id": outfit.outfit_id,
                "user_id": outfit.user_id,
                "subscribe_count": outfit.subscribe_count,
                "total_price": round(total_price, 2),  # Include total price and round to 2 decimals
                "products": products_info,
                "true_tags": list(true_tags)  # Include only the tags that are True
            }

            result.append(outfit_data)

        return jsonify({"user_id": user_id, "outfits": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@outfits_bp.route('/api/subscribed-outfits', methods=['GET'])
def get_subscribed_outfits():
    user_id = 20
    try:
        subscriptions = db.session.query(OutfitSubscription).filter_by(user_id=user_id).all()

        if not subscriptions:
            return jsonify({"error": f"No subscribed outfits found for user {user_id}"}), 404

        result = []
        for subscription in subscriptions:
            outfit = subscription.outfit  # Access the subscribed outfit
            if outfit:
                product_categories = ['shirt', 'pant', 'accessory', 'shoe', 'outerwear', 'dress']
                products_info = []
                true_tags = set()  # Collect tags that are True across all products
                total_price = 0  # Initialize total price for the outfit

                for category in product_categories:
                    product_obj = getattr(outfit, category)
                    if product_obj:
                        total_price += product_obj.price

                        season_style_dict = (
                            {
                                "Fall": product_obj.season_style.Fall,
                                "Winter": product_obj.season_style.Winter,
                                "Spring": product_obj.season_style.Spring,
                                "Summer": product_obj.season_style.Summer,
                                "Casual": product_obj.season_style.Casual,
                                "Business": product_obj.season_style.Business,
                                "Sport": product_obj.season_style.Sport
                            }
                            if product_obj.season_style
                            else None
                        )

                        if season_style_dict:
                            true_tags.update(
                                [key for key, value in season_style_dict.items() if value]
                            )

                        product_dict = {
                            "ProductID": product_obj.ProductID,
                            "gender": product_obj.gender,
                            "masterCategory": product_obj.masterCategory,
                            "subCategory": product_obj.subCategory,
                            "articleType": product_obj.articleType,
                            "baseColour": product_obj.baseColour,
                            "year": product_obj.year,
                            "usage": product_obj.usage,
                            "productDisplayName": product_obj.productDisplayName,
                            "image_url": product_obj.image_url,
                            "price": product_obj.price,
                            "favorite": product_obj.favorite,
                            "category": category,
                            "season_style": season_style_dict  # Include all tags
                        }

                        products_info.append(product_dict)

                outfit_data = {
                    "outfit_id": outfit.outfit_id,
                    "user_id": outfit.user_id,
                    "subscribe_count": outfit.subscribe_count,
                    "total_price": round(total_price, 2),
                    "products": products_info,
                    "true_tags": list(true_tags)  # Include only the tags that are True
                }

                result.append(outfit_data)

        return jsonify({"user_id": user_id, "subscribed_outfits": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@outfits_bp.route('/api/unsave_outfit', methods=['POST'])
def unsave_outfit():
    data = request.json

    # if 'user_id' not in data or 'outfit_id' not in data:
    #     return jsonify({'error': 'Missing user_id or outfit_id'}), 400

    user_id = 20
    outfit_id = data['outfit_id']

    try:
        outfit = Outfit.query.get(outfit_id)
        if not outfit:
            return jsonify({'error': 'Outfit does not exist'}), 404

        existing_subscription = OutfitSubscription.query.filter_by(user_id=user_id, outfit_id=outfit_id).first()
        if not existing_subscription:
            return jsonify({'message': 'User is not subscribed to this outfit.'}), 200

        outfit.subscribe_count -= 1
        db.session.delete(existing_subscription)
        db.session.commit()

        return jsonify({
            'message': 'User unsubscribed from outfit successfully!',
            'outfit_id': outfit_id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@outfits_bp.route('/api/check-outfit/<int:outfit_id>', methods=['GET'])
def get_products_of_outfit(outfit_id):
    user_id = 20
    try:
        outfit = db.session.query(Outfit).filter_by(outfit_id=outfit_id).first()

        if not outfit:
            return jsonify({"error": f"No outfit found with outfit_id {outfit_id}"}), 404

        product_categories = ['shirt', 'pant', 'accessory', 'shoe', 'outerwear', 'dress']
        products_info = []
        total_price = 0
        true_tags = set()

        for category in product_categories:
            product_obj = getattr(outfit, category)
            if product_obj:
                total_price += product_obj.price
                is_product_subscribed = db.session.query(ProductSubscription).filter_by(
                    user_id=user_id, product_id=product_obj.ProductID).first() is not None

                season_style_dict = {
                    "Fall": product_obj.season_style.Fall,
                    "Winter": product_obj.season_style.Winter,
                    "Spring": product_obj.season_style.Spring,
                    "Summer": product_obj.season_style.Summer,
                    "Casual": product_obj.season_style.Casual,
                    "Business": product_obj.season_style.Business,
                    "Sport": product_obj.season_style.Sport
                }
                true_tags.update([key for key, value in season_style_dict.items() if value])

                product_dict = {
                    "ProductID": product_obj.ProductID,
                    "articleType": product_obj.articleType,
                    "baseColour": product_obj.baseColour,
                    "category": category,
                    "favorite": product_obj.favorite,
                    "gender": product_obj.gender,
                    "image_url": product_obj.image_url,
                    "masterCategory": product_obj.masterCategory,
                    "price": product_obj.price,
                    "productDisplayName": product_obj.productDisplayName,
                    "season_style": season_style_dict,
                    "subCategory": product_obj.subCategory,
                    "usage": product_obj.usage,
                    "year": product_obj.year,
                    "is_subscribed": is_product_subscribed
                }

                products_info.append(product_dict)

        outfit_data = {
            "outfit_id": outfit.outfit_id,
            "products": products_info,
            "subscribe_count": outfit.subscribe_count,
            "total_price": round(total_price, 2),
            "true_tags": list(true_tags),
            "user_id": user_id
        }
        return jsonify({
            "outfits": outfit_data,
            "user_id": user_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500