from abc import ABC, abstractclassmethod

class DirectMessageDataManagerInterface(ABC):
    @abstractclassmethod
    def create_direct_message(self, sender_id, receiver_id, content):
        pass
    
    @abstractclassmethod
    def get_direct_messages_by_id(self, receiver_id):
        pass
    
    @abstractclassmethod
    def get_all_direct_messages(self):
        pass
    