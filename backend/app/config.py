from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    if os.getenv('ENV') == 'DEVELOPMENT':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    else:
        host = os.getenv('MYSQL_HOST')
        user = user=os.getenv('MYSQL_USER')
        password=os.getenv('MYSQL_PASSWORD')
        database=os.getenv('MYSQL_DB')
        
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'
    
    JWT_SECRET_KEY = 'abcd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
