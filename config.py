import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    app_key = os.getenv("app_key")
    data_base_url = os.getenv("data_base_url")
    
    JWT_SECRET_KEY = f'{app_key}'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'{data_base_url}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False