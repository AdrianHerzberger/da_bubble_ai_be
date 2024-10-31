from flask import Blueprint, jsonify, request
from ..storage.channel_user_association_data_manager import ChannelUserAssociationManager
from ..instances.db_instance import db

channel_user_association_routes = Blueprint("channel_user_association_routes", __name__)
channel_user_association_data_manager = ChannelUserAssociationManager(db)

@channel_user_association_routes.route("/create_user_association_to_channel", methods=["POST"])
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


@channel_user_association_routes.route("/channel_associated_user/<int:user_id>", methods=["GET"])
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


@channel_user_association_routes.route("/user_associated_channel/<int:channel_id>", methods=["GET"])
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