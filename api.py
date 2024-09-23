from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from config import Config
from storage.db_instance import db
from storage.user_data_manager import UserDataManager
from storage.channel_data_manager import ChannelDataManager
from storage.channel_user_association_data_manager import ChannelUserAssociationManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
CORS(app) 

user_data_manager = UserDataManager(db)
channel_data_manager = ChannelDataManager(db)
channel_user_association_data_manager =  ChannelUserAssociationManager(db)

SWAGGER_URL = "/api/docs"
API_URL = "/static/blogcms.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Blog CMS API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = user_data_manager.get_user_by_id(user_id)
    try:  
        if user:
            return jsonify({
                "id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_profile_picture_url": user.user_profile_picture_url
            })
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data by id: {e}")
        return jsonify({"error": "Failed to get user data by id"}), 500
    
    
@app.route("/api/users/<user_email>", methods=["GET"])
def get_user_by_email(user_email):
    user = user_data_manager.get_user_by_email(user_email)
    try:
        if user:
            return jsonify({
                "id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_profile_picture_url": user.user_profile_picture_url
            })
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data by email: {e}")
        return jsonify({"error": "Failed to get user data by email"}), 500

    
@app.route("/api/all_users", methods=["GET"])
def get_all_user():
    users = user_data_manager.get_all_users()
    print(f"Get all users : {users}")
    try: 
        if users:
            user_list = []
            for user in users:
                user_data = {
                    "id" : user.id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                    "user_profile_picture_url": user.user_profile_picture_url
                }
                user_list.append(user_data)
            return jsonify(user_list)
        else:
            return jsonify({"error": "Users not found"}), 404
    except Exception as e:
        print(f"Error getting all user data: {e}")
        return jsonify({"error": "Failed to get all user data"}), 500
        
    
@app.route("/api/register_user", methods=["POST"])
def register_user():
    data = request.get_json()
    user_email = data.get('user_email')
    user_name = data.get('user_name')
    user_password = data.get('user_password')
    
    try:
        new_user = user_data_manager.create_user(user_email, user_name, user_password)
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
    user_profile_picture_url = data.get("user_profile_picture_url")
    user = user_data_manager.get_user_by_email(user_email)
    
    try:
        if user and user_data_manager.check_user_password(user_password, user.user_password):
            user_data_manager.update_user_profile_picture(user.id, user_profile_picture_url)
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            return jsonify({
                "message" : "Sign-in successfully",
                "user_id" : user.id,
                "user_name" : user.user_name,
                "user_profile_picture_url": user.user_profile_picture_url,
                "access_token": access_token
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to login user"}), 500
    
    
@app.route("/api/create_channel", methods=["POST"])
@jwt_required()
def create_channel():
    data = request.get_json()
    channel_name = data.get("channel_name")
    channel_description = data.get("channel_description")
    channel_color = data.get("channel_color")
    
    user_id = get_jwt_identity()
    
    try:
        new_channel = channel_data_manager.create_channel(channel_name, channel_description, channel_color, user_id)
        print(f"Result if channel: {new_channel}")
        return jsonify({"message": "Channel created successfully"}), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500
    
         
if __name__ == "__main__":
    app.run(debug=True, port=5001)

