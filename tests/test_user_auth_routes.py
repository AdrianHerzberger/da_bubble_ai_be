import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from flask import Flask
from app.routes.user_routes import user_routes
from flask_jwt_extended import JWTManager
from config import Config


class TestUserAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(user_routes)
        cls.app.config["JWT_SECRET_KEY"] = Config.super_secret
        cls.app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        cls.app.config["JWT_HEADER_NAME"] = "Authorization" 
        cls.app.config["JWT_HEADER_TYPE"] = "Bearer"
        JWTManager(cls.app)
        cls.client = cls.app.test_client()


    @patch("app.routes.auth_routes.UserDataManager.get_user_by_email")
    @patch("app.routes.auth_routes.UserDataManager.check_user_password")
    @patch("app.routes.auth_routes.create_access_token")
    @patch("app.routes.auth_routes.create_refresh_token")
    async def test_valid_login(self, mock_create_refresh_token, mock_create_access_token, mock_check_user_password, mock_get_user_by_email):
        mock_get_user_by_email.return_value = MagicMock(
            id="c62fed14-8e82-44bb-9a74-361115f6e2d6",
            user_name="Test User",
            user_password="hashed_password"
        )
        mock_check_user_password.return_value = True
        mock_create_access_token.return_value = "access_token_123"
        mock_create_refresh_token.return_value = "refresh_token_123"

        payload = {
            "user_email": "test@example.com",
            "user_password": "validPassword123"
        }

        response = await self.client.post("/login", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn("access_token_123", response.get_data(as_text=True))
        self.assertIn("refresh_token_123", response.get_data(as_text=True))

    
    @patch("app.routes.auth_routes.UserDataManager.get_user_by_email")
    @patch("app.routes.auth_routes.UserDataManager.check_user_password")
    async def test_invalid_password_login(self, mock_check_user_password, mock_get_user_by_email):
        mock_get_user_by_email.return_value = MagicMock(
            id="c62fed14-8e82-44bb-9a74-361115f6e2d6",
            user_name="Test User",
            user_password="hashed_password"
        )

        mock_check_user_password.return_value = False

        payload = {
            "user_email": "test@example.com",
            "user_password": "wrongPassword123!"
        }

        response = await self.client.post("/login", json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to login user", response.get_data(as_text=True))


    @patch("app.routes.auth_routes.UserDataManager.get_user_by_email")
    async def test_error_handling(self, mock_get_user_by_email):
        mock_get_user_by_email.side_effect = Exception("Database connection error")

        payload = {
            "user_email": "test@example.com",
            "user_password": "testPassword123"
        }

        response = await self.client.post("/login", json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to login user", response.get_data(as_text=True))





    


