# init_db.py
import os
import csv
import re
import random
from dotenv import load_dotenv
from app import create_app, db
from app.model import Product, Shirt, Pant, Accessory, Shoe, Outerwear, Dress, SeasonStyle, User, UserProductOutfit

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
    # Random waist length between 25 and 40 inches
    return round(random.uniform(25.0, 40.0), 2)

def random_size_in_cm():
    # Random size between 10 and 100 cm
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
    # Random True/False for seasons and styles
    return SeasonStyle(
        Fall=bool(random.getrandbits(1)),
        Winter=bool(random.getrandbits(1)),
        Spring=bool(random.getrandbits(1)),
        Summer=bool(random.getrandbits(1)),
        Casual=bool(random.getrandbits(1)),
        Business=bool(random.getrandbits(1)),
        Sport=bool(random.getrandbits(1))
    )

def create_user_and_attach_clothing(user_id, num_items_per_category=50):
    # Create the user
    user = User(user_id=user_id, email=f"user{user_id}@example.com", password="securepassword")
    db.session.add(user)

    # Counter to assign unique outfit IDs
    outfit_id_counter = 1

    # Get 50 random items of each category and attach them to the user
    categories = [Shirt, Pant, Accessory, Shoe, Outerwear, Dress]
    for category in categories:
        items = category.query.limit(num_items_per_category).all()
        for item in items:
            user_product_outfit = UserProductOutfit(
                user_id=user_id,
                product_id=item.ProductID,
                outfit_id=outfit_id_counter  # Assign explicit ID
            )
            db.session.add(user_product_outfit)
            outfit_id_counter += 1

    db.session.commit()

def insert_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            product_id = int(row[0]) if row[0].isdigit() else None
            gender = row[1]
            masterCategory = row[2]
            subCategory = row[3]
            articleType = row[4]
            baseColour = row[5]
            season = row[6]
            year = int(row[7]) if row[7].isdigit() else None
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
                # season=season,
                year=year,
                usage=usage,
                productDisplayName=productDisplayName,
                image_url=image_url,
                price=round(random.uniform(20, 150), 2),
                favorite=False
            )
            db.session.add(product)
            db.session.flush()  # So we get ProductID assigned

            # Insert season/style data
            season_style = random_season_style()
            season_style.ProductID = product.ProductID
            db.session.add(season_style)

            # Determine the category and insert into corresponding table
            category = get_category(row)
            if category == "shirts":
                # Assign random Material
                shirt = Shirt(ProductID=product.ProductID, Material=random_material())
                db.session.add(shirt)
            elif category == "pants":
                # Assign random WaistLength
                pant = Pant(ProductID=product.ProductID, WaistLength=random_waist_length())
                db.session.add(pant)
            elif category == "accessories":
                # Assign random SizeinCM
                accessory = Accessory(ProductID=product.ProductID, SizeinCM=random_size_in_cm())
                db.session.add(accessory)
            elif category == "shoes":
                # Assign random Comfort value
                shoe = Shoe(ProductID=product.ProductID, Comfort=random_comfort())
                db.session.add(shoe)
            elif category == "outerwear":
                # Assign random Thickness
                outer = Outerwear(ProductID=product.ProductID, Thickness=random_thickness())
                db.session.add(outer)
            elif category == "dresses":
                # Assign random Design
                dress = Dress(ProductID=product.ProductID, Design=random_design())
                db.session.add(dress)

        db.session.commit()

def print_table_data(model, table_name):
    print(f"\nData in {table_name} table:")
    results = model.query.all()
    for row in results:
        # Print dictionary representation of row excluding internal attributes
        row_dict = {c.name: getattr(row, c.name) for c in row.__table__.columns}
        print(row_dict)

if __name__ == "__main__":
    # If you want to start fresh each time, uncomment these lines:
    # db.drop_all()
    # db.create_all()

    insert_data_from_csv('dataset.csv')
    print("Database initialized and data inserted successfully!")

    create_user_and_attach_clothing(user_id=20, num_items_per_category=50)
    print("Made user with clothes")
    # print_table_data(Product, 'products')
    # print_table_data(Shirt, 'shirts')
    # print_table_data(Pant, 'pants')
    # print_table_data(Accessory, 'accessories')
    # print_table_data(Shoe, 'shoes')
    # print_table_data(Outerwear, 'outerwear')
    # print_table_data(Dress, 'dresses')
