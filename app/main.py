from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from .routes.user_routes import user_routes
from .routes.channel_routes import channel_routes
from .routes.channel_user_association_routes import channel_user_association_routes
from .routes.channel_message_routes import channel_message_routes
from .instances.db_instance import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize db with the app
db.init_app(app)

# Initialize jwt Manager in the app
jwt = JWTManager(app)

SWAGGER_URL = "/api/docs"
API_URL = "/app/static/da_bubble.json"
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "DA_Bubble_API"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Register blueprints
app.register_blueprint(user_routes, url_prefix="/api")
app.register_blueprint(channel_routes, url_prefix="/api")
app.register_blueprint(channel_user_association_routes, url_prefix="/api")
app.register_blueprint(channel_message_routes, url_prefix="/api")
