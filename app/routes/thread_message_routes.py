import asyncio
from flask import Blueprint, jsonify, request
from ..storage.thread_message_data_manager import ThreadMessageDataManager
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import datetime

thread_message_routes = Blueprint("thread_message_routes", __name__)
thread_message_manager = ThreadMessageDataManager()

@thread_message_routes.route("/create_message_thread", methods=["POST"])
async def create_message_thread():
    data = request.get_json()
    thread_type = data.get("thread_type")
    channel_message_id = data.get("channel_message_id")
    direct_message_id = data.get("direct_message_id")
    thread_suggestion = data.get("thread_suggestion")
    content = data.get("content")
    
    try:
        new_message = await thread_message_manager.create_thread(
            thread_type, channel_message_id, direct_message_id, content, thread_suggestion
        )
        
        if new_message:
            return jsonify({"message": "Message created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create message"}), 404
        
    except Exception as e:
        print(f"Error creating message: {e}")
        return jsonify({"error": "Server error"}), 500
    
    
@thread_message_routes.route("/get_thread_messages_channel_id/<channel_message_id>", methods=["GET"])
async def get_thread_messages_channel_id(channel_message_id):
    try:
        thread_message = await thread_message_manager.get_thread_messages_channel_id(channel_message_id)
        print(f"Result of thread messages: {thread_message}")
        if thread_message:
            return jsonify({
                "id": thread_message.id,
                "thread_type": thread_message.thread_type,
                "content": thread_message.content,
                "thread_suggestion": thread_message.thread_suggestion
            }), 200
        else:
            return jsonify({"error": "Thread message data not found"}), 404      
    except Exception as e:
        print(f"Error getting thread message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500        
            
