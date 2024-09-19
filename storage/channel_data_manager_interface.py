from abc import ABC, abstractclassmethod

class ChannelDataManagerInterface(ABC):
    @abstractclassmethod
    def create_channel(self, channel_name, channel_description, channel_color, user_id):
        pass