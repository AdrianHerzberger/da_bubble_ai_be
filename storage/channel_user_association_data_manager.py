from models.channel_user_association_model import db, ChannelUserAssociation
from .channel_user_association_data_manager_interface import ChannelUserAssociationInterface
from sqlalchemy.exc import SQLAlchemyError


class ChannelUserAssociationManager(ChannelUserAssociationInterface):
    def __init__(self, db_instance):
        self.db = db_instance

    def create_channel_user_association(self, user_id, channel_id):
        try:
            new_channel_user_association = ChannelUserAssociation(
                user_id=user_id,
                channel_id=channel_id
            )
            self.db.session.add(new_channel_user_association)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error creating channel user association: {e}")
            self.db.session.rollback()
            return False

    def get_all_users_in_channel(self, channel_id):
        channel = ChannelUserAssociation.query(
            Channel).filter_by(id=channel_id).first()

        users_in_channel = channel.users
        for user in users_in_channel:
            print(user.user_name, user.user_email)

    def get_channel_associated_user(self, user_id):
        try:
            associations = ChannelUserAssociation.query.filter_by(user_id=user_id).all()
            
            channels_for_user = []
            for association in associations:
                channel = association.channel 
                channels_for_user.append({
                    "channel_id": channel.id,
                    "channel_name": channel.channel_name,
                    "channel_description": channel.channel_description,
                    "channel_color": channel.channel_color
                })
            return channels_for_user
        except SQLAlchemyError as e:
            print(f"Error fetching channels for user {user_id}: {e}")
            return None