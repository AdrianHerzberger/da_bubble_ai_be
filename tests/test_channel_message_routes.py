import unittest
from unittest.mock import patch, AsyncMock
from flask import Flask
from app.routes.channel_message_routes import channel_message_routes
from flask_jwt_extended import JWTManager, create_access_token
from config import Config
from datetime import datetime


class MockMessage:
    def __init__(self, id, channel_id, sender_id, content, timestamp):
        self.id = id
        self.channel_id = channel_id
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp

class ChannelMessageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(channel_message_routes)
        cls.app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
        cls.app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        cls.app.config["JWT_HEADER_NAME"] = "Authorization" 
        cls.app.config["JWT_HEADER_TYPE"] = "Bearer"
        JWTManager(cls.app)
        cls.client = cls.app.test_client()
        print(cls.app.url_map)


    @patch("app.routes.channel_message_routes.ChannelMessageDataManager.create_message")
    def test_create_channel_message(self, mock_create_message):

        mock_channel_message = AsyncMock(id="83b95aa4-e8ab-4c57-82f3-a7a2a3704837")
        mock_create_message.return_value = mock_channel_message

        payload = {
            "sender_id": "e94dc166-1a64-4a3a-bff4-b36dd1d0b843",
            "content": "Test message to send for channels" 
        }

        with self.app.test_client() as client:
            response = client.post(f"/create_message_channel/{mock_channel_message.id}", json=payload)

        print(f"Response: {response.status_code}, Data: {response.get_data(as_text=True)}")

        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertEqual(response_data["message"], "Message created successfully")
        self.assertEqual(response_data["message_id"], "83b95aa4-e8ab-4c57-82f3-a7a2a3704837")


    @patch("app.routes.channel_message_routes.ChannelMessageDataManager.delete_channel_message")
    def test_delete_channel_message(self, mock_delete_channel_message):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        mock_delete_channel_message.return_value = True

        test_channel_message_id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        headers = {"Authorization": f"Bearer {access_token}"} 

        response = self.client.delete(f"/delete_channel_message/{test_channel_message_id}", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Channel message deleted successfully", response.get_data(as_text=True))
        mock_delete_channel_message.assert_awaited_once_with(test_channel_message_id)

    
    @patch("app.routes.channel_message_routes.ChannelMessageDataManager.update_channel_message")
    def test_update_channel_message(self, mock_update_channel_message):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        mock_update_channel_message.return_value = True

        test_update_channel_message_id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        headers={"Authorization": f"Bearer {access_token}"}

        payload = {
            "update_content": "Updated Test Message for specific channel",
        }

        response = self.client.patch(f"/update_channel_message/{test_update_channel_message_id}", headers=headers, json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Channel message updated successfully", response.get_data(as_text=True))
        mock_update_channel_message.assert_awaited_once_with(test_update_channel_message_id, payload["update_content"])
        

    @patch("app.routes.channel_message_routes.ChannelMessageDataManager.get_all_channel_messages")
    def test_get_channel_messages_success(self, mock_get_channel_messages):
        mock_channel_messages = [
            MockMessage(
                id="83b95aa4-e8ab-4c57-82f3-a7a2a3704837",
                channel_id="0ea65395-5342-4a34-b329-ead94ce446a5",
                sender_id="e94dc166-1a64-4a3a-bff4-b36dd1d0b843",
                content="First test channel message which will be mocked",
                timestamp=datetime(2024, 11, 25, 10, 56, 12, 995386)
            ),
            MockMessage(
                id="cd18d10b-002e-44e6-bcbb-3e62da6b3c86",
                channel_id="0ea65395-5342-4a34-b329-ead94ce446a5",
                sender_id="e94dc166-1a64-4a3a-bff4-b36dd1d0b843",
                content="Second test channel message which will be mocked",
                timestamp=datetime(2024, 11, 25, 10, 56, 12, 995386),
            ),
        ]
        mock_get_channel_messages.return_value = mock_channel_messages

        expected_data =  {
            'count': 2, 
            'is_next_page': False, 
            'results': [
                {
                    'channel_id': '0ea65395-5342-4a34-b329-ead94ce446a5', 
                    'content': 'First test channel message which will be mocked', 
                    'message_id': '83b95aa4-e8ab-4c57-82f3-a7a2a3704837', 
                    'message_time': '2024-11-25T10:56:12.995386', 
                    'sender_id': 'e94dc166-1a64-4a3a-bff4-b36dd1d0b843'
                }, 
                {
                    'channel_id': '0ea65395-5342-4a34-b329-ead94ce446a5', 
                    'content': 'Second test channel message which will be mocked', 
                    'message_id': 'cd18d10b-002e-44e6-bcbb-3e62da6b3c86', 
                    'message_time': '2024-11-25T10:56:12.995386', 
                    'sender_id': 'e94dc166-1a64-4a3a-bff4-b36dd1d0b843'
                }
            ], 
            'total_pages': 1
        }

        response = self.client.get(
            "/get_all_channel_messages/?page_number=1&page_size=2"
        )

        print("Actual response JSON:", response.get_json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_data)


    @patch("app.routes.channel_message_routes.ChannelMessageDataManager.get_all_channel_messages")
    def test_failed_channel_messages(self, mock_get_all_channel_messages):
        mock_get_all_channel_messages.return_value = []
        response = self.client.get("/get_all_channel_messages/?page_number=1&page_size=2")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Channel messages not found"})









