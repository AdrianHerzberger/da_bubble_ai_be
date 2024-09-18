from .user_storage import db, User
from .data_manager_interface import DataManagerInterface
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash


class PostgreSQLDataManager(DataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance

    def create_user(self, user_email, user_name, user_password):
        hashed_password = generate_password_hash(user_password)

        new_user = User(
            user_email=user_email,
            user_name=user_name,
            user_password=hashed_password,
        )

        self.db.session.add(new_user)
        self.db.session.commit()

    def get_user(self, user_name, user_password):
        user = User.query.filter_by(user_name=user_name).first()
        if user and check_password_hash(user.user_password, user_password):
            return user
        return None

    def get_user_by_id(self, id):
        user_id_query = User.query.filter_by(id=id).first()
        return user_id_query

    def get_user_by_email(self, user_email):
        user_email_query = User.query.filter_by(user_email=user_email).first()
        return user_email_query

    def check_user_password(self, user_password, stored_hashed_password):
        return check_password_hash(stored_hashed_password, user_password)
