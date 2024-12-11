# init_db.py
import os
import csv
import re
import random
from dotenv import load_dotenv
from app import create_app, db
from app.model import (
    Product, Shirt, Pant, Accessory, Shoe, Outerwear, Dress,
    SeasonStyle, User, Outfit, OutfitSubscription, ProductSubscription
)

load_dotenv()
env = os.getenv('ENV')

app = create_app()
app.app_context().push()  # Ensure we are in an application context

# Keyword categories with regex patterns to determine which category a product falls into
keyword_categories = {
    "shirts": [r'\b\w*shirt\w*\b', r'\b\w*top\w*\b'],
    "pants": [r'\b\w*short\w*\b', r'\b\w*jean\w*\b', r'\b\w*pant\w*\b', r'\b\w*trunk\w*\b', r'\b\w*jogger\w*\b', r'\b\w*trouser\w*\b', r'\b\w*chino\w*\b', r'\b\w*cargo\w*\b'],
    "accessories": [r'\b\w*bag\w*\b', r'\b\w*necklace\w*\b', r'\b\w*jewelry\w*\b', r'\b\w*ring\w*\b', r'\b\w*cufflink\w*\b', r'\b\w*sunglass\w*\b', r'\b\w*belt\w*\b'],
    "shoes": [r'\b\w*flat\w*\b', r'\b\w*sneaker\w*\b', r'\b\w*shoe\w*\b', r'\b\w*sandal\w*\b', r'\b\w*slipper\w*\b', r'\b\w*flip flops\w*\b'],
    "outerwear": [r'\b\w*jacket\w*\b', r'\b\w*hoodie\w*\b', r'\b\w*sweater\w*\b', r'\b\w*cardigan\w*\b'],
    "dresses": [r'\b\w*dress\w*\b', r'\b\w*saree\w*\b']
}

def get_category(row):
    for category, patterns in keyword_categories.items():
        for pattern in patterns:
            if any(re.search(pattern, field, re.IGNORECASE) for field in row):
                return category
    return None

def random_material():
    materials = ["Cotton", "Polyester", "Linen", "Silk", "Wool", "Rayon"]
    return random.choice(materials)

def random_waist_length():
    return round(random.uniform(25.0, 40.0), 2)

def random_size_in_cm():
    return round(random.uniform(10.0, 100.0), 2)

def random_comfort():
    comforts = ["Very Comfortable", "Comfortable", "Moderate", "Uncomfortable"]
    return random.choice(comforts)

def random_thickness():
    thicknesses = ["Lightweight", "Medium", "Heavy"]
    return random.choice(thicknesses)

def random_design():
    designs = ["Floral", "Striped", "Solid", "Polka Dot", "Abstract"]
    return random.choice(designs)

def random_season_style():
    return SeasonStyle(
        Fall=bool(random.getrandbits(1)),
        Winter=bool(random.getrandbits(1)),
        Spring=bool(random.getrandbits(1)),
        Summer=bool(random.getrandbits(1)),
        Casual=bool(random.getrandbits(1)),
        Business=bool(random.getrandbits(1)),
        Sport=bool(random.getrandbits(1))
    )

def insert_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            product_id = int(row[0]) if row[0].isdigit() else None
            gender = row[1]
            masterCategory = row[2]
            subCategory = row[3]
            articleType = row[4]
            baseColour = row[5]
            # season = row[6]  # Not used in current models
            year = int(row[7]) if row[7].isdigit() else 2000
            usage = row[8]
            productDisplayName = row[9]
            image_url = row[10]

            product = Product(
                ProductID=product_id,
                gender=gender,
                masterCategory=masterCategory,
                subCategory=subCategory,
                articleType=articleType,
                baseColour=baseColour,
                year=year,
                usage=usage,
                productDisplayName=productDisplayName,
                image_url=image_url,
                price=round(random.uniform(20, 150), 2),
                favorite=False
            )
            db.session.add(product)
            db.session.flush()  # Assigns ProductID if not provided

            # Insert season/style data
            season_style = random_season_style()
            season_style.ProductID = product.ProductID
            db.session.add(season_style)

            # Determine category and insert into corresponding table
            category = get_category(row)
            if category == "shirts":
                shirt = Shirt(ProductID=product.ProductID, Material=random_material())
                db.session.add(shirt)
            elif category == "pants":
                pant = Pant(ProductID=product.ProductID, WaistLength=random_waist_length())
                db.session.add(pant)
            elif category == "accessories":
                accessory = Accessory(ProductID=product.ProductID, SizeinCM=random_size_in_cm())
                db.session.add(accessory)
            elif category == "shoes":
                shoe = Shoe(ProductID=product.ProductID, Comfort=random_comfort())
                db.session.add(shoe)
            elif category == "outerwear":
                outer = Outerwear(ProductID=product.ProductID, Thickness=random_thickness())
                db.session.add(outer)
            elif category == "dresses":
                dress = Dress(ProductID=product.ProductID, Design=random_design())
                db.session.add(dress)

    db.session.commit()
    print("Products and related categories inserted successfully.")

def create_users_and_subscriptions(num_users=50, num_products_per_category=50):
    # Fetch all users
    users = []
    for i in range(1, num_users + 1):
        user = User(email=f"user{i}@example.com", password="securepassword")
        db.session.add(user)
        users.append(user)
    db.session.commit()
    print(f"Created {num_users} users.")

    # Fetch all products per category
    shirts_all = db.session.query(Product).join(Shirt).all()
    pants_all = db.session.query(Product).join(Pant).all()
    shoes_all = db.session.query(Product).join(Shoe).all()
    accessories_all = db.session.query(Product).join(Accessory).all()

    total_users = len(users)
    if total_users < 1:
        print("No users available to subscribe to outfits.")
        return

    for user in users:
        # Randomly select products for the user's closet
        user_shirts = random.sample(shirts_all, min(num_products_per_category, len(shirts_all))) if shirts_all else []
        user_pants = random.sample(pants_all, min(num_products_per_category, len(pants_all))) if pants_all else []
        user_shoes = random.sample(shoes_all, min(num_products_per_category, len(shoes_all))) if shoes_all else []
        user_accessories = random.sample(accessories_all, min(num_products_per_category, len(accessories_all))) if accessories_all else []

        # Subscribe the user to these products (their "closet")
        for p in user_shirts + user_pants + user_shoes + user_accessories:
            ps = ProductSubscription(user_id=user.user_id, product_id=p.ProductID)
            db.session.add(ps)
        db.session.commit()
        print(f"Subscribed user {user.user_id} to their closet items.")

        # Create one outfit for the user from a random product in each category
        shirt_product = random.choice(user_shirts) if user_shirts else None
        pant_product = random.choice(user_pants) if user_pants else None
        shoe_product = random.choice(user_shoes) if user_shoes else None
        accessory_product = random.choice(user_accessories) if user_accessories else None

        if shirt_product and pant_product and shoe_product and accessory_product:
            outfit = Outfit(
                user_id=user.user_id,
                shirt_id=shirt_product.ProductID,
                pant_id=pant_product.ProductID,
                shoe_id=shoe_product.ProductID,
                accessory_id=accessory_product.ProductID,
                subscribe_count=1  # Initialize with 1 for the owner
            )
            db.session.add(outfit)
            db.session.commit()
            print(f"Created an outfit for user {user.user_id}.")

            # Subscribe the owner to their own outfit
            outfit_subscription = OutfitSubscription(user_id=user.user_id, outfit_id=outfit.outfit_id)
            db.session.add(outfit_subscription)
            db.session.commit()
            print(f"User {user.user_id} subscribed to their own outfit {outfit.outfit_id}.")

            # Assign additional subscriptions to reach a random subscribe_count between 1 and 50
            random_subscribe_count = random.randint(1, 50)
            additional_subscriptions_needed = random_subscribe_count - 1  # Already subscribed by owner

            if additional_subscriptions_needed > 0:
                # Select random users to subscribe (excluding the owner)
                possible_subscribers = [u for u in users if u.user_id != user.user_id]
                if len(possible_subscribers) < additional_subscriptions_needed:
                    selected_subscribers = possible_subscribers
                else:
                    selected_subscribers = random.sample(possible_subscribers, additional_subscriptions_needed)

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
                print(f"Outfit {outfit.outfit_id} subscribed by {outfit.subscribe_count} users.")
        else:
            print(f"Insufficient products to create an outfit for user {user.user_id}.")

def print_table_data(model, table_name):
    print(f"\nData in {table_name} table:")
    results = model.query.all()
    for row in results:
        row_dict = {c.name: getattr(row, c.name) for c in row.__table__.columns}
        print(row_dict)

if __name__ == "__main__":
    # Uncomment the following lines if you want to reset the database
    # db.drop_all()
    # db.create_all()

    insert_data_from_csv('dataset.csv')
    print("Database initialized and products inserted successfully.")

    create_users_and_subscriptions(num_users=50, num_products_per_category=50)
    print("Users and their closets created with outfits and subscriptions.")

    # Optional: Print sample data for verification
    # print_table_data(OutfitSubscription, 'outfit_subscriptions')
    # print_table_data(ProductSubscription, 'product_subscriptions')

    print("Setup complete with 50 users")
