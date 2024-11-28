from abc import ABC, abstractclassmethod

class ChannelMessageDataManagerInterface(ABC):
    @abstractclassmethod
    def create_message(self, channel_id, sender_id, content):
        pass
    
    @abstractclassmethod
    def get_channel_messages_by_id(self, channel_id):
        pass
     
    @abstractclassmethod
    def get_all_channel_messages(self):
        pass
    