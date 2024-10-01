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
from storage.channel_message_manager import ChannelMessageManager
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

user_data_manager = UserDataManager(db)
channel_data_manager = ChannelDataManager(db)
channel_user_association_data_manager = ChannelUserAssociationManager(db)
channel_message_manager = ChannelMessageManager(db)

SWAGGER_URL = "/api/docs"
API_URL = "/static/blogcms.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Blog CMS API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/api/get_user_by_id/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = user_data_manager.get_user_by_id(user_id)

    try:
        if user:
            return jsonify({
                "user_id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_profile_picture_url": user.user_profile_picture_url
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data by id: {e}")
        return jsonify({"error": "Failed to get user data by id"}), 500


@app.route("/api/get_user_by_email/<user_email>", methods=["GET"])
def get_user_by_email(user_email):
    user = user_data_manager.get_user_by_email(user_email)
    try:
        if user:
            return jsonify({
                "user_id": user.id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_profile_picture_url": user.user_profile_picture_url
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user data by email: {e}")
        return jsonify({"error": "Failed to get user data by email"}), 500


@app.route("/api/all_users", methods=["GET"])
def get_all_user():
    users = user_data_manager.get_all_users()

    try:
        if users:
            user_list = []
            for user in users:
                user_data = {
                    "user_id": user.id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                    "user_profile_picture_url": user.user_profile_picture_url
                }
                user_list.append(user_data)
            return jsonify(user_list), 200
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
        new_user = user_data_manager.create_user(
            user_email, user_name, user_password)
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
            user_data_manager.update_user_profile_picture(
                user.id, user_profile_picture_url)
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(hours=1))
            return jsonify({
                "message": "Sign-in successfully",
                "user_id": user.id,
                "user_name": user.user_name,
                "user_profile_picture_url": user.user_profile_picture_url,
                "access_token": access_token
            }), 201
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
        new_channel = channel_data_manager.create_channel(
            channel_name, channel_description, channel_color, user_id)

        if new_channel:
            return jsonify({
                "message": "Channel created successfully",
                "channel_id": new_channel.id
            }), 201
        else:
            return jsonify({"error": "Failed to create channel"}), 500
    except Exception as e:
        print(f"Error creating channel: {e}")
        return jsonify({"error": "Failed to create channel"}), 500


@app.route("/api/get_channel_by_id/<int:channel_id>", methods=["GET"])
def get_channel_by_id(channel_id):
    channel = channel_data_manager.get_channel_by_id(channel_id)

    try:
        if channel:
            return jsonify({
                "channel_id": channel.id,
                "channel_name": channel.channel_name,
                "channel_description": channel.channel_description,
                "channel_color": channel.channel_color,
            })
        else:
            return jsonify({"error": "Channel not found"}), 404
    except Exception as e:
        print(f"Error getting channel data by id: {e}")
        return jsonify({"error": "Failed to get channel data by id"}), 500


@app.route("/api/all_channels", methods=["GET"])
def get_all_channels():
    channels = channel_data_manager.get_all_channels()

    try:
        if channels:
            channel_list = []
            for channel in channels:
                channel_data = {
                    "channel_id": channel.id,
                    "channel_name": channel.channel_name,
                    "channel_description": channel.channel_description,
                    "channel_color": channel.channel_color
                }
                channel_list.append(channel_data)
            return jsonify(channel_list), 200
        else:
            return jsonify({"error": "Channel data not found"}), 404
    except Exception as e:
        print(f"Error getting channel data: {e}")
        return jsonify({"error": "Failed to get channel data"}), 500


@app.route("/api/create_user_association_to_channel", methods=["POST"])
def create_user_association_to_channel():
    data = request.get_json()
    user_ids = data.get("user_id")
    channel_id = data.get("channel_id")

    if not isinstance(user_ids, list):
       
        return jsonify({"error": "user_id must be a list"}), 400

    try:
        for user_id in user_ids:
            print(f"The user ID´s passed from the frontend {user_id}")
            new_user_association = channel_user_association_data_manager.create_channel_user_association(
                user_id, channel_id
            )
            if not new_user_association:
                return jsonify({"error": f"Failed to associate user {user_id} with channel {channel_id}"}), 500

        return jsonify({
            "message": "Channel user associations created successfully",
            "user_ids": user_ids,
            "channel_id": channel_id
        }), 201

    except Exception as e:
        print(f"Error creating user association to channel: {e}")
        return jsonify({"error": "Failed to create channel user associations"}), 500


@app.route("/api/channel_associated_user/<int:user_id>", methods=["GET"])
def get_channel_associated_user(user_id):
    channels_for_user = channel_user_association_data_manager.get_channel_associated_user(
        user_id)

    try:
        if channels_for_user:
            return jsonify(channels_for_user), 200
        else:
            return jsonify({"error": "No channels found for this user"}), 404
    except Exception as e:
        print(f"Error getting channel data: {e}")
        return jsonify({"error": "Failed to get channel data"}), 500


@app.route("/api/user_associated_channel/<int:channel_id>", methods=["GET"])
def user_associated_channel(channel_id):
    users_for_channel = channel_user_association_data_manager.get_user_associated_channel(
        channel_id)

    try:
        if users_for_channel:
            return jsonify(users_for_channel), 200
        else:
            return jsonify({"error": "No users found for this channel"}), 404
    except Exception as e:
        print(f"Error getting user data: {e}")
        return jsonify({"error": "Failed to get users data"}), 500


@app.route("/api/create_message_channel", methods=["POST"])
def create_message_channel():
    data = request.get_json()
    channel_id = data.get("channel_id")
    sender_id = data.get("sender_id")
    content = data.get("content")
    timestamp_str  = data.get("timestamp")

    try:
        if isinstance(timestamp_str, str):
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            print(timestamp)
        else:
            return jsonify({"error": "Invalid timestamp format"}), 400

        new_message = channel_message_manager.create_message(channel_id, sender_id, content, timestamp)

        if new_message:
            return jsonify({"message": "Message created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create message"}), 500

    except Exception as e:
        print(f"Error creating message for channel: {e}")
        return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)

