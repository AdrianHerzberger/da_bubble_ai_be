from abc import ABC, abstractclassmethod

class ChannelMessageManagerInterface(ABC):
    @abstractclassmethod
    def create_message(self, channel_id, sender_id, content, timestmap):
        pass