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
            return new_channel_user_association
        except Exception as e:
            print(f"Error creating channel user association: {e}")
            self.db.session.rollback()
            return None

    def get_all_users_in_channel(self, channel_id):
        channel = ChannelUserAssociation.query(
            Channel).filter_by(id=channel_id).first()

        users_in_channel = channel.users
        for user in users_in_channel:
            print(user.user_name, user.user_email)

    def get_channel_associated_users(self, user_id):
        user = ChannelUserAssociation.query(User).filter_by(id=user_id).first()

        channels_for_user = user.channels
        for channel in channels_for_user:
            print(channel.channel_name, channel.channel_description)
