import unittest
from unittest.mock import patch, AsyncMock
from flask import Flask
from app.routes.channel_routes import channel_routes
from flask_jwt_extended import JWTManager, create_access_token
from config import Config


class ChannelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(channel_routes)
        cls.app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
        cls.app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        cls.app.config["JWT_HEADER_NAME"] = "Authorization" 
        cls.app.config["JWT_HEADER_TYPE"] = "Bearer"
        JWTManager(cls.app)
        cls.client = cls.app.test_client()
        print(cls.app.url_map)


    @patch("app.routes.channel_routes.ChannelDataManager.create_channel", new_callable=AsyncMock)
    @patch("app.routes.channel_routes.ChannelUserAssociationManager.create_channel_user_association", new_callable=AsyncMock)
    def test_create_channel(self, mock_create_channel_user_association, mock_create_channel):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        mock_channel = AsyncMock(id="0ea65395-5342-4a34-b329-ead94ce446a5")
        mock_create_channel.return_value = mock_channel

        headers = {"Authorization": f"Bearer {access_token}"} 
        payload = {
            "channel_name": "Test ChannelName",
            "channel_description": "A test description for a channel",
        }

        with self.app.test_client() as client:
            response = client.post("/create_channel", headers=headers, json=payload) 

        print(f"Response: {response.status_code}, Data: {response.get_data(as_text=True)}")

        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertEqual(response_data["message"], "Channel created successfully")
        self.assertEqual(response_data["channel_id"], "0ea65395-5342-4a34-b329-ead94ce446a5")

        mock_create_channel.assert_called_once_with(
            "Test ChannelName", "A test description for a channel", "test_user"
        )
        mock_create_channel_user_association.assert_called_once_with(
            "test_user", "0ea65395-5342-4a34-b329-ead94ce446a5"
        )


    @patch("app.routes.channel_routes.ChannelDataManager.get_channel_by_id")
    def test_get_channel_by_id(self, mock_get_channel_by_id):

        mock_channel = AsyncMock()
        mock_channel.id = "0ea65395-5342-4a34-b329-ead94ce446a5"
        mock_channel.channel_name = "Test Channel"
        mock_channel.channel_description = "A Test Channel for Unittest"
        mock_channel.channel_color = "d83be2"

        mock_get_channel_by_id.return_value = mock_channel

        response = self.client.get(f"/get_channel_by_id/{mock_channel.id}")
        
        print(f"Response: {response.status_code}, Data: {response.get_data(as_text=True)}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Channel", response.get_data(as_text=True))
        self.assertIn("A Test Channel for Unittest", response.get_data(as_text=True))
        mock_get_channel_by_id.assert_awaited_once_with("0ea65395-5342-4a34-b329-ead94ce446a5")


    @patch("app.routes.channel_routes.ChannelDataManager.get_all_channels")
    def test_get_all_channels(self, mock_get_all_channels):
        
        mock_channels = [
            {
                "channel_id": "2fb515b9-d052-43e0-a196-bc8c3289fe06",
                "channel_name": "General",
                "channel_description": "General discussion",
                "channel_color": "blue"
            },
            {
                "channel_id": "bb919724-f17b-45d0-a84a-6327e1726b05",
                "channel_name": "Announcements",
                "channel_description": "Official announcements",
                "channel_color": "red"
            }
        ]

        mock_get_all_channels.return_value = mock_channels

        response = self.client.get(f"/get_all_channels")

        self.assertEqual(response.status_code, 200)
        expected_data = [
            {
                "channel_id": "2fb515b9-d052-43e0-a196-bc8c3289fe06",
                "channel_name": "General",
                "channel_description": "General discussion",
                "channel_color": "blue"
            },
            {
                "channel_id": "bb919724-f17b-45d0-a84a-6327e1726b05",
                "channel_name": "Announcements",
                "channel_description": "Official announcements",
                "channel_color": "red"
            }
        ]
        self.assertEqual(response.json, expected_data)

    @patch("app.routes.channel_routes.ChannelDataManager.get_all_channels")
    def test_get_all_channels_no_channels(self, mock_get_all_channels):
        mock_get_all_channels.return_value = []
        response = self.client.get("/get_all_channels")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Channel data not found"})


