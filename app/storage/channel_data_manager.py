from ..instances.db_instance import db 
from ..models.channel_model import Channel
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
            return None
        
    def get_channel_by_id(self, channel_id):
        channel_id_query = Channel.query.filter_by(id=channel_id).first()
        return channel_id_query
    
    def get_all_channels(self):
        all_channels = Channel.query.all()
        return all_channels