import unittest
import time
from unittest.mock import AsyncMock, patch
from flask import Flask
from app.routes.user_routes import user_routes
from app.routes.auth_routes import auth_routes
from flask_jwt_extended import JWTManager, create_access_token
from config import Config


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(user_routes)
        cls.app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
        cls.app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        cls.app.config["JWT_HEADER_NAME"] = "Authorization" 
        cls.app.config["JWT_HEADER_TYPE"] = "Bearer"
        JWTManager(cls.app)
        cls.client = cls.app.test_client()

    @patch("app.routes.user_routes.UserDataManager.create_user")
    def test_register_user(self, mock_create_user):
        mock_create_user.return_value = {"user_id": "c62fed14-8e82-44bb-9a74-361115f6e2d6"}

        payload = {
            "user_email": "test@example.com",
            "user_name": "Test User",
            "user_password": "testPassword123%$"
        }

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

        response = self.client.get(f"/get_user_by_id/{mock_user.id}")

        print(f"Response: {response.status_code}, Data: {response.get_data(as_text=True)}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", response.get_data(as_text=True))
        self.assertIn("john.doe@example.com", response.get_data(as_text=True))
        mock_get_user_by_id.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")


    @patch("app.routes.user_routes.UserDataManager.get_user_by_email")
    def test_get_user_by_email(self, mock_get_user_by_email):

        mock_user = AsyncMock()
        mock_user.id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        mock_user.user_name = "Jane Doe"
        mock_user.user_email = "jane.doe@example.com"
        mock_user.user_profile_picture_url = "jane.com/profile.jpg"

        mock_get_user_by_email.return_value = mock_user

        response = self.client.get("get_user_by_email/jane.doe@example.com")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Doe", response.get_data(as_text=True))
        self.assertIn("jane.doe@example.com", response.get_data(as_text=True))
        mock_get_user_by_email.assert_awaited_once_with("jane.doe@example.com")


    @patch("app.routes.user_routes.UserDataManager.delete_user", new_callable=AsyncMock)
    def test_delete_user_success_with_valid_jwt(self, mock_delete_user):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        mock_delete_user.return_value = True 
        
        test_user_id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        headers = {"Authorization": f"Bearer {access_token}"}  

        response = self.client.delete(f"/delete_user/{test_user_id}", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted successfully", response.get_data(as_text=True))
        mock_delete_user.assert_awaited_once_with(test_user_id)


    @patch("app.routes.user_routes.UserDataManager.delete_user")
    def test_delete_user_not_found(self, mock_delete_user):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        mock_delete_user.return_value = False

        test_user_id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        headers = {"Authorization": f"Bearer {access_token}"}  

        response = self.client.delete(f"/delete_user/{test_user_id}", headers=headers)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.get_data(as_text=True))
        mock_delete_user.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")


    @patch("app.routes.user_routes.UserDataManager.update_user", new_callable=AsyncMock)
    def test_update_user(self, mock_update_user):
        with self.app.app_context():
            access_token = create_access_token(identity="test_user")

        mock_update_user.return_value = True

        test_user_id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        headers={"Authorization": f"Bearer {access_token}"}

        payload = {
            "update_user_name": "John DoeTest",
        }

        response = self.client.patch(f"/update_user/{test_user_id}", headers=headers, json=payload)

        print(f"Response: {response.status_code}, Data: {response.get_data(as_text=True)}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("User updated successfully", response.get_data(as_text=True))
        mock_update_user.assert_awaited_once_with(test_user_id, payload["update_user_name"])


        









