import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:adrian123@localhost:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app_key = os.getenv("app_key")
    JWT_SECRET_KEY = f'{app_key}'