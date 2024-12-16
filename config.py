import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    app_key = os.getenv("app_key")
    super_secret = os.getenv("jwt_secret_key")
    data_base_url = os.getenv("data_base_url")
    render_data_base_url= os.getenv("render_data_base_url")
    url_host = os.getenv("url_host")
    elastic_key = os.getenv("elastic_key")
    
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', f'{super_secret}')
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', f'{data_base_url}')
    RENDER_DATA_BASE_URL = os.getenv('RENDER_URL', f'{render_data_base_url}')
    ELASTIC_SEARCH_HOST = os.getenv('HOST_URL', f'{url_host}')
    ELASTIC_KEY = os.getenv('ELASTIC_KEY', f'{elastic_key}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False