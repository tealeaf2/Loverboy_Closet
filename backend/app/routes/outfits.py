from flask import Blueprint, jsonify
from app.model import Outfit, Product, OutfitSubscription
from app import db

outfits_bp = Blueprint('outfits', __name__)

@outfits_bp.route('/api/user/<int:user_id>/outfits', methods=['GET'])
def get_user_outfits(user_id):
    user_id = 20
    try:
        # Query all outfits for the given user
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
        # Query all subscribed outfits for the given user
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

        return jsonify({"user_id": user_id, "subscribed_outfits": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500