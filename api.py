from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from storage.db_instance import db
from storage.data_base_manager import PostgreSQLDataManager
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
data_manager = PostgreSQLDataManager(db)

CORS(app) 

SWAGGER_URL = "/api/docs"
API_URL = "/static/blogcms.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Blog CMS API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = data_manager.get_user_by_id(user_id)
    try:  
        if user:
            return jsonify({
                "id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email
            })
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data: {e}")
        return jsonify({"error": "Failed to get user data"}), 500
    
    
@app.route("/api/users/<user_email>", methods=["GET"])
def get_user_by_email(user_email):
    user = data_manager.get_user_by_email(user_email)
    if user:
        return jsonify({
            "id": user.id,
            "user_name": user.user_name,
            "user_email": user.user_email
        })
    else:
        return jsonify({"error": "User not found"}), 404

    
@app.route("/api/register_user", methods=["POST"])
def register_user():
    data = request.get_json()
    user_email = data.get('user_email')
    user_name = data.get('user_name')
    user_password = data.get('user_password')
    
    try:
        new_user = data_manager.create_user(user_email, user_name, user_password)
        print(f"Result if user: {new_user}")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500
    

@app.route("/api/sign_in_user", methods=["POST"])
def sign_in_user():
    data = request.get_json()
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    
    user = data_manager.get_user_by_email(user_email)
    
    try:
        if user and data_manager.check_user_password(user_password, user.user_password):
            return jsonify({
                "message" : "Sign-in successfully",
                "user_id" : user.id,
                "user_name" : user.user_name
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to login user"}), 500
        
        
if __name__ == "__main__":
    app.run(debug=True, port=5001)
