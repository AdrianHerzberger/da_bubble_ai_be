from abc import ABC, abstractclassmethod

class ChannelUserAssociationDataManagerInterface(ABC):
    @abstractclassmethod
    def create_channel_user_association(self, user_id, channel_id):
        pass
    
    @abstractclassmethod
    def get_users_for_channel(self, channel_id):
        pass
    
    @abstractclassmethod
    def get_channels_for_user(self, user_id):
        pass