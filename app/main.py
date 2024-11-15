import asyncio
from flask import Flask
from asgiref.wsgi import WsgiToAsgi
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from .routes.user_routes import user_routes
from .routes.channel_routes import channel_routes
from .routes.channel_user_association_routes import channel_user_association_routes
from .routes.channel_message_routes import channel_message_routes
from .routes.role_routes import role_routes
from .routes.summarization_routes import summarization_routes
from .session_management.create_async_engine import AsyncSessionLocal, async_engine, Base
from config import Config
import platform

app = Flask(__name__)
app.config.from_object(Config)
asgi_app = WsgiToAsgi(app)

# Initialize jwt Manager in the app
jwt = JWTManager(app)

SWAGGER_URL = "/api/docs"
API_URL = "/static/da_bubble.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "DA_Bubble_API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Register blueprints
app.register_blueprint(user_routes, url_prefix="/api")
app.register_blueprint(channel_routes, url_prefix="/api")
app.register_blueprint(channel_user_association_routes, url_prefix="/api")
app.register_blueprint(channel_message_routes, url_prefix="/api")
app.register_blueprint(role_routes, url_prefix="/api")
app.register_blueprint(summarization_routes, url_prefix="/api")

# if platform.system() == "Windows":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# # Initialize the database tables asynchronously at startup 
# async def init_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# # Set up the app and initialize async resources before running
# def setup_app():
#     try:
#         asyncio.run(init_db())
#     except RuntimeError as e:
#         print(f"RuntimeError during async setup: {e}")
#         raise

# setup_app()

# Close the async session after each request
# @app.teardown_appcontext
# async def shutdown_session(exception=None):
#     async_session = AsyncSessionLocal()
#     await async_session.close()