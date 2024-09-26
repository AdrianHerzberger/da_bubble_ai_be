from abc import ABC, abstractclassmethod

class ChannelUserAssociationInterface(ABC):
    @abstractclassmethod
    def create_channel_user_association(self, user_ids, channel_id):
        pass
    
    @abstractclassmethod
    def get_user_associated_channel(self, channel_id):
        pass
    
    @abstractclassmethod
    def get_channel_associated_user(self, user_id):
        pass