import asyncio
from flask import Blueprint, jsonify, request
from ..storage.direct_message_data_manager import DirectMessageDataManager
from flask_jwt_extended import jwt_required, get_jwt_identity

direct_message_routes = Blueprint("direct_message_routes", __name__)
direct_message_manager = DirectMessageDataManager()

@direct_message_routes.route("/create_message_direct/<sender_id>", methods=["POST"])
async def create_message_direct(sender_id):
    data = request.get_json()
    receiver_id = data.get("receiver_id")
    content = data.get("content")
    
    if receiver_id is None:
        raise Exception(f"Receiver id must exist, can't preceed to create message")
        return
    
    try:
        new_message = await direct_message_manager.create_direct_message(
            sender_id, receiver_id, content)
        
        if new_message:
            return jsonify({"message": "Message created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create message"}), 404
    except Exception as e:
        print(f"Error creating message for channel: {e}")
        return jsonify({"error": "Server error"}), 500
    
    
@direct_message_routes.route("/get_direct_message_by_id/<receiver_id>", methods=["GET"])
async def get_direct_message_by_id(receiver_id):
    try:
        direct_message = await direct_message_manager.get_direct_message_by_id(receiver_id)
        if direct_message:
            direct_message_list = []
            for message in direct_message:
                direct_message_data = {
                    "message_id": message.id,
                    "sender_id": message.sender_id,
                    "receiver_id": message.receiver_id,
                    "content": message.content,
                    "message_time": message.timestamp
                }
                direct_message_list.append(direct_message_data)
            return jsonify(direct_message_list), 200
        else:
            return jsonify({"error": "Direct message data not found"}), 404
    except Exception as e:
        print(f"Error getting direct message data: {e}")
        return jsonify({"error": "Failed to get direct message data"}), 500
    

@direct_message_routes.route("/get_all_direct_messages", methods=["GET"])
async def get_all_direct_messages():
    try:
        direct_messages = await direct_message_manager.get_all_direct_messages()
        if direct_messages:
            direct_message_list = []
            for message in direct_messages:
                direct_message_data = {
                    "message_id": message.id,
                    "sender_id": message.sender_id,
                    "receiver_id": message.receiver_id,
                    "content": message.content,
                    "message_time": message.timestamp
                }
                direct_message_list.append(direct_message_data)
            return jsonify(direct_message_list), 200
        else:
            return jsonify({"error": "Direct messages not found"}), 404
    except Exception as e:
        print(f"Error getting direct message data: {e}")
        return jsonify({"error": "Failed to get direct message data"}), 500
    
                