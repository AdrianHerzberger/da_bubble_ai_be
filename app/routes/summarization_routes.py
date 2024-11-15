import asyncio
from flask import Blueprint, jsonify, request
from ..utils.summarization_provider import Summarization

summarization_routes = Blueprint("summarization_routes", __name__)

@summarization_routes.route("/summarize", methods=["POST"])
async def summarize():
    try:
        summarization = Summarization()
        summarization_result = summarization.summarization_result()
        return jsonify({"filtered_keywords": summarization_result}), 201
    except Exception as e:
        print(f"Error providing keywords: {e}")
        return jsonify({"error": "Failed to provide extracted keywords"})