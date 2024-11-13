from flask import Blueprint, jsonify, request
from ..storage.channel_user_association_data_manager import ChannelUserAssociationManager
from ..instances.db_instance import db

channel_user_association_routes = Blueprint(
    "channel_user_association_routes", __name__)
channel_user_association_data_manager = ChannelUserAssociationManager()


@channel_user_association_routes.route("/create_user_association_to_channel", methods=["POST"])
async def create_user_association_to_channel():
    data = request.get_json()
    user_ids = data.get("user_id")
    channel_id = data.get("channel_id")

    if not isinstance(user_ids, list):
        return jsonify({"error": "user_id must be a list"}), 400

    try:
        for user_id in user_ids:
            new_user_association = await channel_user_association_data_manager.create_channel_user_association(
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


@channel_user_association_routes.route("/get_users_for_channel/<channel_id>", methods=["GET"])
async def get_users_for_channel(channel_id):
    try:
        users = await channel_user_association_data_manager.get_users_for_channel(channel_id)
        print(f"The result of found users : {users}")
        if users:
            return jsonify(users), 200
        else:
            return jsonify({"error": "No users found for this channel"}), 404
    except Exception as e:
        print(f"Error fetching users for channel: {e}")
        return jsonify({"error": "Failed to fetch users"}), 500


@channel_user_association_routes.route("/get_channels_for_user/<user_id>", methods=["GET"])
async def get_channels_for_user(user_id):
    try:
        channels = await channel_user_association_data_manager.get_channels_for_user(user_id)
        print(f"The result of found channels : {channels}")

        if channels:
            return jsonify(channels), 200
        else:
            return jsonify({"error": "No channels found for this user"}), 404
    except Exception as e:
        print(f"Error fetching channels for user: {e}")
        return jsonify({"error": "Failed to fetch channels"}), 500
