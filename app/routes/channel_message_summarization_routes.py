from flask import Blueprint, jsonify
from ..utils.summarization_provider import Summarization
from ..services.thread_suggestion_management import MessageThreadSuggestion
from ..services.sentiment_suggestion_managment import SentimentSuggestion
from ..storage.channel_message_data_manager import ChannelMessageDataManager

channel_message_summarization_routes = Blueprint("summarization_routes", __name__)
channel_message_manager = ChannelMessageDataManager()


@channel_message_summarization_routes.route("/get_channel_messages/<channel_id>/summarization", methods=["GET"])
async def channel_messages_summarization(channel_id):
    try:
        channel_messages = await channel_message_manager.get_channel_messages_by_id(channel_id)
        if channel_messages:       
            contextual_insights = MessageThreadSuggestion()
            keywords = contextual_insights.extract_keywords(channel_messages)
            
            if keywords:
                summarization = Summarization()
                summarized_keywords = summarization.filter_summarization(keywords)
                return jsonify(summarized_keywords)
            else:
                return jsonify({"error": "Channel message data not found"}), 404
    except Exception as e:
        print(f"Error getting channel message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500


@channel_message_summarization_routes.route("/get_channel_messages/<channel_id>/suggestion", methods=["GET"])
async def  channel_messages_suggetion(channel_id):
    try:
        channel_messages = await channel_message_manager.get_channel_messages_by_id(channel_id)
        if channel_messages:
            sentiment_suggestions = SentimentSuggestion()
            suggestion = sentiment_suggestions.analyze_sentiment(channel_messages)

            if suggestion:
                return jsonify(suggestion)
        else:
                return jsonify({"error": "Channel message data not found"}), 404
    except Exception as e:
        print(f"Error getting channel message data: {e}")
        return jsonify({"error": "Failed to get channel message data"}), 500

