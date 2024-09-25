from abc import ABC, abstractclassmethod

class ChannelUserAssociationInterface(ABC):
    @abstractclassmethod
    def create_channel_user_association(self, channel_id, user_id):
        pass
    
    @abstractclassmethod
    def get_all_users_in_channel(self, channel_id):
        pass
    
    @abstractclassmethod
    def get_channel_associated_user(self, user_id):
        pass