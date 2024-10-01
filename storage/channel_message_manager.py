from models.channel_model import db, ChannelMessage
from .channel_message_manager_interface import ChannelMessageManagerInterface
from sqlalchemy.exc import SQLAlchemyError

class ChannelMessageManager(ChannelMessageManagerInterface):
    def __init__(self, db_instance):
        self.db = db_instance
        
    def create_message(self, channel_id, sender_id, content, timestamp):
        try: 
            new_message = ChannelMessage(
                channel_id=channel_id,
                sender_id=sender_id,
                content=content,
                timestamp=timestamp,
            )
            self.db.session.add(new_message)
            self.db.session.commit()
            return True
        
        except Exception as e:
            print(f"Error creating user: {e}")
            self.db.session.rollback()
            return None