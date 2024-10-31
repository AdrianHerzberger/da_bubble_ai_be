from ..instances.db_instance import db 
from ..models.user_model import User
from .user_data_manager_interface import UserDataManagerInterface
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash


class UserDataManager(UserDataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance

    def create_user(self, user_email, user_name, user_password):
        hashed_password = generate_password_hash(user_password)
        
        try:
            new_user = User(
                user_email=user_email,
                user_name=user_name,
                user_password=hashed_password,
            )
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user     
        except Exception as e:
            print(f"Error creating user: {e}")
            self.db.session.rollback()
            return None
        
    def get_all_users(self):
        all_users = User.query.all()
        return all_users

    def get_user(self, user_name, user_password):
        user = User.query.filter_by(user_name=user_name).first()
        if user and check_password_hash(user.user_password, user_password):
            return user
        return None

    def get_user_by_id(self, user_id):
        user_id_query = User.query.filter_by(id=user_id).first()
        return user_id_query

    def get_user_by_email(self, user_email):
        user_email_query = User.query.filter_by(user_email=user_email).first()
        return user_email_query

    def check_user_password(self, user_password, stored_hashed_password):
        return check_password_hash(stored_hashed_password, user_password)
    
    def update_user_profile_picture(self, user_id, user_profile_picture_url):
        try:
            user_id_query = User.query.filter_by(id=user_id).first()
            if user_id_query:
                user_id_query.user_profile_picture_url = user_profile_picture_url
                self.db.session.commit()
                return True
        except Exception as e:
            print(f"Error updating user profile picture: {e}")
            self.db.session.rollback()
            return False