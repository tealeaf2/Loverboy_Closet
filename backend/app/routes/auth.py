from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db
from ..model import Product, Shirt, Pant, Accessory, Shoe, OutfitSubscription, ProductSubscription, Outfit, User
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register():
    """
    Registers a new user.
    Accepts JSON payload: { "email": "user@example.com", "password": "password123" }
    Returns success or error message.
    """
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Email and password are required"}), 400

    email = data['email']
    password = data['password']

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email is already registered"}), 400

    # Hash the password and create the user
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    # Fetch all products per category
    shirts_all = db.session.query(Product).join(Shirt).all()
    pants_all = db.session.query(Product).join(Pant).all()
    shoes_all = db.session.query(Product).join(Shoe).all()
    accessories_all = db.session.query(Product).join(Accessory).all()

    # Number of products to subscribe to per category (adjustable)
    num_products_per_category = 50

    # Randomly select products for the user's closet
    user_shirts = random.sample(shirts_all, min(num_products_per_category, len(shirts_all))) if shirts_all else []
    user_pants = random.sample(pants_all, min(num_products_per_category, len(pants_all))) if pants_all else []
    user_shoes = random.sample(shoes_all, min(num_products_per_category, len(shoes_all))) if shoes_all else []
    user_accessories = random.sample(accessories_all, min(num_products_per_category, len(accessories_all))) if accessories_all else []

    # Subscribe the user to these products (their "closet")
    for p in user_shirts + user_pants + user_shoes + user_accessories:
        ps = ProductSubscription(user_id=new_user.user_id, product_id=p.ProductID)
        db.session.add(ps)
    db.session.commit()

    # Create one outfit for the user from a random product in each category
    shirt_product = random.choice(user_shirts) if user_shirts else None
    pant_product = random.choice(user_pants) if user_pants else None
    shoe_product = random.choice(user_shoes) if user_shoes else None
    accessory_product = random.choice(user_accessories) if user_accessories else None

    if shirt_product and pant_product and shoe_product and accessory_product:
        outfit = Outfit(
            user_id=new_user.user_id,
            shirt_id=shirt_product.ProductID,
            pant_id=pant_product.ProductID,
            shoe_id=shoe_product.ProductID,
            accessory_id=accessory_product.ProductID,
            subscribe_count=1  # Initialize with 1 for the owner
        )
        db.session.add(outfit)
        db.session.commit()

        # Subscribe the owner to their own outfit
        outfit_subscription = OutfitSubscription(user_id=new_user.user_id, outfit_id=outfit.outfit_id)
        db.session.add(outfit_subscription)
        db.session.commit()

        # Assign additional subscriptions to reach a random subscribe_count between 1 and 50
        random_subscribe_count = random.randint(1, 50)
        additional_subscriptions_needed = random_subscribe_count - 1  # Already subscribed by owner

        if additional_subscriptions_needed > 0:
            # Select random users to subscribe (excluding the owner)
            possible_subscribers = [u for u in User.query.all() if u.user_id != new_user.user_id]
            selected_subscribers = random.sample(possible_subscribers, min(len(possible_subscribers), additional_subscriptions_needed))

            for subscriber in selected_subscribers:
                # Check if already subscribed to avoid duplicates
                existing_subscription = db.session.query(OutfitSubscription).filter_by(
                    user_id=subscriber.user_id, outfit_id=outfit.outfit_id
                ).first()
                if not existing_subscription:
                    os = OutfitSubscription(user_id=subscriber.user_id, outfit_id=outfit.outfit_id)
                    db.session.add(os)
                    outfit.subscribe_count += 1
            db.session.commit()

    return jsonify({"message": "User registered and closet created successfully"}), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    """
    Logs in a user.
    Accepts JSON payload: { "email": "user@example.com", "password": "password123" }
    Returns a JWT token if successful.
    """
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Email and password are required"}), 400

    email = data['email']
    password = data['password']

    # Verify user exists
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401
    
    # Generate JWT token
    access_token = jwt.encode({"user_id": user.user_id}, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": access_token}), 200