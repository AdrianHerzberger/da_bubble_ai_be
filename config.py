import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    app_key = os.getenv("app_key")
    super_secret = os.getenv("jwt_secret_key")
    data_base_url = os.getenv("data_base_url")
    
    JWT_SECRET_KEY = f'{super_secret}'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'{data_base_url}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False