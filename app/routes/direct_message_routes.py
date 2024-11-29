from flask import Blueprint, jsonify, request
from ..storage.direct_message_data_manager import DirectMessageDataManager
from ..utils.pagination_offset import PaginationOffset
from ..models.direct_message_model import DirectMessage
from ..configuartions.direct_message_serializer import DirectMessageSerializer

direct_message_routes = Blueprint("direct_message_routes", __name__)
direct_message_manager = DirectMessageDataManager()

@direct_message_routes.route("/create_message_direct/<sender_id>", methods=["POST"])
async def create_message_direct(sender_id):
    data = request.get_json()
    receiver_id = data.get("receiver_id")
    content = data.get("content")
    
    if receiver_id is None:
        raise Exception(f"Receiver id must exist, can't preceed to create message")
    
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
        direct_messages = await direct_message_manager.get_direct_messages_by_id(receiver_id)
        if not direct_messages:
            return jsonify({"error": "Direct messages not found"}), 404

        page_number = int(request.args.get("page_number", 1))
        page_size = int(request.args.get("page_size", 10))

        paginator = PaginationOffset(page_number=page_number, page_size=page_size)

        context = {}

        paginated_direct_messages_response = paginator(DirectMessage, direct_messages, DirectMessageSerializer, context)

        if paginated_direct_messages_response:
            return jsonify(paginated_direct_messages_response), 200

        elif direct_messages:
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
    
                