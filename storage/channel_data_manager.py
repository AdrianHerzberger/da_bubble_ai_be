from .channel_storage import db, Channel
from .channel_data_manager_interface import ChannelDataManagerInterface
from sqlalchemy.exc import SQLAlchemyError

class ChannelDataManager(ChannelDataManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance
        
    def create_channel(self, channel_name, channel_description, channel_color, user_id):
        try:
            new_channel = Channel(
                channel_name=channel_name,
                channel_description=channel_description,
                channel_color=channel_color,
                user_id=user_id
            )
            self.db.session.add(new_channel)
            self.db.session.commit()
            return new_channel 
        except Exception as e:
            print(f"Error creating channel: {e}")
            self.db.session.rollback()
            return False