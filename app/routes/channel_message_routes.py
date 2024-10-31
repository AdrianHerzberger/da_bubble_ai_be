from flask import Blueprint, jsonify, request
from ..storage.channel_message_manager import ChannelMessageManager
from ..instances.db_instance import db
from datetime import datetime

channel_message_routes = Blueprint("channel_message_routes", __name__)
channel_message_manager = ChannelMessageManager(db)

@channel_message_routes.route("/create_message_channel", methods=["POST"])
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