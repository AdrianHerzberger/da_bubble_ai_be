import unittest
from unittest.mock import AsyncMock, patch
from flask import Flask
from app.routes.user_routes import user_routes


class TestUserStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(user_routes)
        cls.client = cls.app.test_client()

    @patch("app.routes.user_routes.UserDataManager.create_user")
    def test_register_user(self, mock_create_user):
        mock_create_user.return_value = {"user_id": "c62fed14-8e82-44bb-9a74-361115f6e2d6"}

        payload = {
            "user_email": "test@example.com",
            "user_name": "Test User",
            "user_password": "testPassword123%$"
        }

        with self.app.test_request_context(json=payload):
            response = self.client.post("/register_user", json=payload)

        
        self.assertEqual(response.status_code, 201)
        self.assertIn("c62fed14-8e82-44bb-9a74-361115f6e2d6", response.get_data(as_text=True))
        mock_create_user.assert_awaited_once_with(
            "test@example.com", "Test User", "testPassword123%$"
        )

    
    @patch("app.routes.user_routes.UserDataManager.get_user_by_id")
    def test_get_user_by_id(self, mock_get_user_by_id):

        mock_user = AsyncMock()
        mock_user.id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        mock_user.user_name = "John Doe"
        mock_user.user_email = "john.doe@example.com"
        mock_user.user_profile_picture_url = "example.com/profile.jpg"

        mock_get_user_by_id.return_value = mock_user

        response = self.client.get("/get_user_by_id/c62fed14-8e82-44bb-9a74-361115f6e2d6")

        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", response.get_data(as_text=True))
        self.assertIn("john.doe@example.com", response.get_data(as_text=True))
        mock_get_user_by_id.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")

    
    









