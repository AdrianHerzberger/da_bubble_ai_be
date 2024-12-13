from datetime import datetime
import unittest
from unittest.mock import patch, AsyncMock
from flask import Flask
from app.routes.auth_routes import auth_routes
from flask_jwt_extended import JWTManager, create_access_token
from config import Config

class TestUserAuth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(auth_routes) 
        cls.app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
        cls.app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        cls.app.config["JWT_HEADER_NAME"] = "Authorization" 
        cls.app.config["JWT_HEADER_TYPE"] = "Bearer"
        JWTManager(cls.app)
        cls.client = cls.app.test_client()


    @patch("app.routes.auth_routes.UserDataManager.get_user_by_email", new_callable=AsyncMock)
    @patch("app.routes.auth_routes.UserDataManager.check_user_password")
    @patch("app.routes.auth_routes.UserDataManager.update_user_last_login_date", new_callable=AsyncMock)
    def test_valid_login(self, mock_update_user_last_login_date, mock_check_user_password, mock_get_user_by_email):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        last_login_date = datetime.now()

        mock_get_user_by_email.return_value = AsyncMock(
            id="c62fed14-8e82-44bb-9a74-361115f6e2d6",
            user_name="Test User",
            user_password="hashed_password"
        )

        mock_check_user_password.return_value = True
        mock_update_user_last_login_date.return_value = last_login_date

        headers = {"Authorization": f"Bearer {access_token}"} 
        payload = {
            "user_email": "test@example.com",
            "user_password": "validPassword123!"
        }

        response = self.client.post("/login", headers=headers, json=payload)
        response_data = response.get_json()
        self.assertIn("access_token", response_data)
        self.assertIn("refresh_token", response_data)
        self.assertIn("user_id", response_data)
        self.assertIn("user_name", response_data)
        self.assertEqual(response_data["message"], "Login successful")

    
    @patch("app.routes.auth_routes.UserDataManager.get_user_by_email", new_callable=AsyncMock)
    @patch("app.routes.auth_routes.UserDataManager.check_user_password")
    @patch("app.routes.auth_routes.UserDataManager.update_user_last_login_date", new_callable=AsyncMock)
    def test_invalid_password_login(self, mock_update_user_last_login_date, mock_check_user_password, mock_get_user_by_email):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        last_login_date = datetime.now()

        mock_get_user_by_email.return_value = AsyncMock(
            id="c62fed14-8e82-44bb-9a74-361115f6e2d6",
            user_name="Test User",
            user_password="hashed_password"
        )

        mock_check_user_password.return_value = False
        mock_update_user_last_login_date.return_value = last_login_date

        headers = {"Authorization": f"Bearer {access_token}"} 
        payload = {
            "user_email": "test@example.com",
            "user_password": "wrongPassword123!"
        }

        response = self.client.post("/login", headers=headers, json=payload)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data["error"], "Invalid email or password")


    @patch("app.routes.auth_routes.unset_jwt_cookies")
    def test_logout(self, mock_unset_jwt_cookies):
        mock_unset_jwt_cookies.side_effect = lambda response: response
        response = self.client.post("/logout")

        self.assertEqual(response.status_code, 200) 
        response_data = response.get_json()
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Logout successful")

        mock_unset_jwt_cookies.assert_called_once()









    


