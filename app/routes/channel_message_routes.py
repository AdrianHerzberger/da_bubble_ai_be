import asyncio
from flask import Blueprint, jsonify, request
from ..storage.channel_message_manager import ChannelMessageManager
from ..services.thread_suggestion_management import MessageThreadSuggestion
from ..utils.summarization_provider import Summarization

channel_message_routes = Blueprint("channel_message_routes", __name__)
channel_message_manager = ChannelMessageManager()


@channel_message_routes.route("/create_message_channel/<channel_id>", methods=["POST"])
async def create_message_channel(channel_id):
    data = request.get_json()
    sender_id = data.get("sender_id")
    content = data.get("content")
    
    if channel_id is None:
        raise Exception(f"Channel did not exist, can't proceed to create message")
        return

    try:
        new_message = await channel_message_manager.create_message(channel_id, sender_id, content)

        if new_message:
            return jsonify({"message": "Message created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create message"}), 500

    except Exception as e:
        print(f"Error creating message for channel: {e}")
        return jsonify({"error": "Server error"}), 500
    
    
@channel_message_routes.route("/get_channel_messages/<channel_id>", methods=["GET"])
async def get_channel_messages(channel_id):
    try: 
        channel_message = await channel_message_manager.get_channel_messages_by_id(channel_id)
        if channel_message:       
            contextual_insights = MessageThreadSuggestion()
            keywords = contextual_insights.extract_keywords(channel_message)
            
            if keywords:
                summarization = Summarization()
                summarized_keywords = summarization.filter_summarization(keywords)
            else:
                summarized_keywords = []
                print("No keywords to summarize.")
            
            if channel_message:
                channel_message_list = []
                for message in channel_message:
                    channel_message_data = {
                        "message_id": message.id,
                        "channel_id": message.channel_id,
                        "sender_id": message.sender_id,
                        "content": message.content,
                        "message_time": message.timestamp
                    }

                    channel_message_list.append(channel_message_data)
                return jsonify(channel_message_list), 200
            else:
                return jsonify({"error": "Channel message data not found"}), 404
    except Exception as e:
        print(f"Error getting channel message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500        


@channel_message_routes.route("/get_all_messages/", methods=["GET"])
async def get_all_messages():
    try:
        channel_message = await channel_message_manager.get_all_messages()
        if channel_message:
            channel_message_list = []
            for message in channel_message:
                channel_message_data = {
                    "message_id": message.id,
                    "channel_id": message.channel_id,
                    "sender_id": message.sender_id,
                    "content": message.content,
                    "message_time": message.timestamp
                }
                channel_message_list.append(channel_message_data)
            return jsonify(channel_message_list), 200
        else:
            return jsonify({"error": "Channel message data not found"}), 404
    except Exception as e:
        print(f"Error getting channel message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500