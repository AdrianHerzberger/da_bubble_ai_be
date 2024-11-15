import asyncio
from flask import Blueprint, jsonify, request
from ..storage.channel_data_manager import ChannelDataManager
from ..storage.channel_user_association_data_manager import ChannelUserAssociationManager
from flask_jwt_extended import jwt_required, get_jwt_identity

channel_routes = Blueprint("channel_routes", __name__)
channel_data_manager = ChannelDataManager()
channel_user_association_manager = ChannelUserAssociationManager()

@channel_routes.route("/create_channel", methods=["POST"])
@jwt_required()
async def create_channel():
    data = request.get_json()
    channel_name = data.get("channel_name")
    channel_description = data.get("channel_description")

    user_id = get_jwt_identity()

    try:
        new_channel = await channel_data_manager.create_channel(
            channel_name, channel_description, user_id)
        
        if new_channel:
            await channel_user_association_manager.create_channel_user_association(user_id, new_channel.id)
            return jsonify({
                "message": "Channel created successfully",
                "channel_id": new_channel.id
            }), 201
        else:
            return jsonify({"error": "Failed to create channel"}), 500
    except Exception as e:
        print(f"Error creating channel: {e}")
        return jsonify({"error": "Failed to create channel"}), 500


@channel_routes.route("/get_channel_by_id/<channel_id>", methods=["GET"])
async def get_channel_by_id(channel_id):
    try:
        channel = await channel_data_manager.get_channel_by_id(channel_id)
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


@channel_routes.route("/get_all_channels", methods=["GET"])
async def get_all_channels():
    try:
        channels = await channel_data_manager.get_all_channels()
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