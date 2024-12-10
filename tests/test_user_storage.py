import unittest
from unittest.mock import AsyncMock, patch
from flask import Flask
from app.routes.user_routes import user_routes
from flask_jwt_extended import JWTManager
from config import Config


class TestUserStorage(unittest.TestCase):

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

    @patch("app.routes.user_routes.UserDataManager.create_user")
    async def test_register_user(self, mock_create_user):
        mock_create_user.return_value = {"user_id": "c62fed14-8e82-44bb-9a74-361115f6e2d6"}

        payload = {
            "user_email": "test@example.com",
            "user_name": "Test User",
            "user_password": "testPassword123%$"
        }

        with self.app.test_request_context(json=payload):
            response = await self.client.post("/register_user", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn("c62fed14-8e82-44bb-9a74-361115f6e2d6", response.get_data(as_text=True))
        mock_create_user.assert_awaited_once_with(
            "test@example.com", "Test User", "testPassword123%$"
        )


    @patch("app.routes.user_routes.UserDataManager.get_user_by_id")
    async def test_get_user_by_id(self, mock_get_user_by_id):

        mock_user = AsyncMock()
        mock_user.id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        mock_user.user_name = "John Doe"
        mock_user.user_email = "john.doe@example.com"
        mock_user.user_profile_picture_url = "example.com/profile.jpg"

        mock_get_user_by_id.return_value = mock_user

        response = await self.client.get("/get_user_by_id/c62fed14-8e82-44bb-9a74-361115f6e2d6")

        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", response.get_data(as_text=True))
        self.assertIn("john.doe@example.com", response.get_data(as_text=True))
        mock_get_user_by_id.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")


    @patch("app.routes.user_routes.UserDataManager.get_user_by_email")
    async def test_get_user_by_email(self, mock_get_user_by_email):

        mock_user = AsyncMock()
        mock_user.id = "c62fed14-8e82-44bb-9a74-361115f6e2d6"
        mock_user.user_name = "Jane Doe"
        mock_user.user_email = "jane.doe@example.com"
        mock_user.user_profile_picture_url = "jane.com/profile.jpg"

        mock_get_user_by_email.return_value = mock_user

        response = await self.client.get("get_user_by_email/jane.doe@example.com")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Doe", response.get_data(as_text=True))
        self.assertIn("jane.doe@example.com", response.get_data(as_text=True))
        mock_get_user_by_email.assert_awaited_once_with("jane.doe@example.com")


    @patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    @patch("flask_jwt_extended.utils.get_jwt", return_value={"sub": "test_user"})
    async def test_jwt_required(self, mock_get_jwt):
        response = await self.client.get(
            "/test_jwt",
            headers={"Authorization": "Bearer test_token"}, 
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("test_user", response.get_data(as_text=True))  
        mock_get_jwt.assert_called_once()  


    @patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    @patch("flask_jwt_extended.utils.get_jwt", return_value={"sub": "test_user"})
    @patch("app.routes.user_routes.UserDataManager.delete_user")
    async def test_delete_user_success(self, mock_delete_user, mock_get_jwt):
        mock_delete_user.return_value = True 

        response = await self.client.delete(
            "/delete_user/c62fed14-8e82-44bb-9a74-361115f6e2d6",
            headers={"Authorization": "Bearer test_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted successfully", response.get_data(as_text=True))
        mock_delete_user.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")
        mock_get_jwt.assert_called_once()


    @patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    @patch("flask_jwt_extended.utils.get_jwt", return_value={"sub": "test_user"})
    @patch("app.routes.user_routes.UserDataManager.delete_user")
    async def test_delete_user_not_found(self, mock_delete_user, mock_get_jwt):
        mock_delete_user.return_value = False

        response = await self.client.delete(
            "/delete_user/c62fed14-8e82-44bb-9a74-361115f6e2d6",
            headers={"Authorization": "Bearer test_token"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.get_data(as_text=True))
        mock_delete_user.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")
        mock_get_jwt.assert_called_once()


    @patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    @patch("flask_jwt_extended.utils.get_jwt", return_value={"sub": "test_user"})
    @patch("app.routes.user_routes.UserDataManager.update_user")
    async def test_update_user(self, mock_update_user, mock_get_jwt):
        mock_update_user.return_value = {"user_id": "c62fed14-8e82-44bb-9a74-361115f6e2d6"}

        payload = {
            "update_user_name": "John DoeTest",
        }

        with self.app.test_request_context(json=payload):
            response = await self.client.post("/update_user/c62fed14-8e82-44bb-9a74-361115f6e2d6",
            headers={"Authorization": "Bearer test_token"}, json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertIn("User updated successfully", response.get_data(as_text=True))
        mock_update_user.assert_awaited_once_with("c62fed14-8e82-44bb-9a74-361115f6e2d6")
        mock_get_jwt.assert_called_once()

        









