import asyncio
from flask import Flask, request, jsonify
from flask import Blueprint, jsonify, request
from ..storage.channel_message_data_manager import ChannelMessageDataManager
from ..utils.channel_message_search_query import search_messages

search_query_routes = Blueprint("search_query_routes", __name__)
channel_message_manager = ChannelMessageDataManager()

@search_query_routes.route("/search/<channel_id>", methods=["GET"])
async def search_term(channel_id):
    data = request.get_json()
    keyword = data.get("keyword")
    
    if not keyword:
        return jsonify({"error" : "Keyword parameter is missing"}), 400
    
    try:
        search_results = await search_messages(channel_id, keyword)
        if not search_results: 
            print(f"No search results found: {search_results}")
            
            messages = await channel_message_manager.get_channel_messages_by_id(channel_id, search_index=search_results)
            
            search_result_list = []
            for message in messages:
                if keyword in message.content.lower():
                    search_data = {
                        {
                            "id": message.id, 
                            "content": message.content, 
                            "timestamp": message.timestamp.isoformat()
                        }
                    }
                    search_result_list.append(search_data)
            return jsonify(search_result_list), 200
        
        return jsonify(search_results), 200
    except Exception as e:
        print(f"Error couldn't find message for channel: {e}")
        return jsonify({"error": "Server error"}), 500

