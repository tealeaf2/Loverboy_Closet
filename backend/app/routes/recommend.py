# recommend.py
from flask import Blueprint, jsonify, request
from app.model import Outfit, Product, OutfitSubscription
from app import db
from app.auth_utils import decode_token

recommend_bp = Blueprint('recommend', __name__)

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
    

@recommend_bp.route('/api/outfits', methods=['GET'])
def get_all_outfits():
    user_id, error_response = get_user_from_token()
    if error_response:
        return error_response
    try:
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        subscribed_outfit_ids = db.session.query(OutfitSubscription.outfit_id).filter_by(user_id=user_id).all()
        subscribed_outfit_ids = {id[0] for id in subscribed_outfit_ids}  # Convert to set for faster lookup

        outfits = db.session.query(Outfit).filter(~Outfit.outfit_id.in_(subscribed_outfit_ids)).all()

        if not outfits:
            return jsonify({"error": "No outfits found"}), 404

        result = []
        for outfit in outfits:
            product_categories = ['shirt', 'pant', 'accessory', 'shoe', 'outerwear', 'dress']
            products_info = []
            true_tags = set()
            total_price = 0
            favorited_items_count = 0  # Counter for favorited items

            for category in product_categories:
                product_obj = getattr(outfit, category)
                if product_obj:
                    total_price += product_obj.price
                    if product_obj.favorite:
                        favorited_items_count += 1  # Increment if the product is favorited

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
                        "season_style": season_style_dict
                    }

                    products_info.append(product_dict)

            outfit_data = {
                "outfit_id": outfit.outfit_id,
                "user_id": outfit.user_id,
                "subscribe_count": outfit.subscribe_count,
                "total_price": round(total_price, 2),  # Include total price and round to 2 decimals
                "products": products_info,
                "true_tags": list(true_tags),  # Include only the tags that are True
                "favorited_items_count": favorited_items_count  # Include the count of favorited items
            }

            result.append(outfit_data)

        # Sort by favorited items count first, then by subscribe count
        result.sort(key=lambda x: (x['favorited_items_count'], x.get('subscribe_count', 0)), reverse=True)

        return jsonify({"outfits": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

@recommend_bp.route('/api/save_outfit', methods=['POST'])
def save_outfit():
    data = request.json

    # Validate required fields
    if 'outfit_id' not in data:
        return jsonify({'error': 'Missing outfit_id'}), 400

    user_id, error_response = get_user_from_token()
    if error_response:
        return error_response
    outfit_id = data['outfit_id']

    try:
        # Check if the outfit exists
        outfit = Outfit.query.get(outfit_id)
        if not outfit:
            return jsonify({'error': 'Outfit does not exist'}), 404
        
        # Check if the subscription already exists
        existing_subscription = OutfitSubscription.query.filter_by(user_id=user_id, outfit_id=outfit_id).first()
        if existing_subscription:
            return jsonify({'message': 'User is already subscribed to this outfit.'}), 200

        outfit.subscribe_count += 1
        # Create a new subscription
        subscription = OutfitSubscription(user_id=user_id, outfit_id=outfit_id)
        db.session.add(subscription)
        db.session.commit()

        return jsonify({
            'message': 'User subscribed to outfit successfully!',
            'outfit_id': outfit_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500