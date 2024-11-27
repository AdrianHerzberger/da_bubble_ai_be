from abc import ABC, abstractclassmethod

class ThreadMessageDataManagerInterface(ABC):
    @abstractclassmethod
    def create_thread(self, thread_type, channel_message_id, direct_message_id, content, thread_suggestion):
        pass
    
    @abstractclassmethod
    def get_thread_messages_channel_id(self, channel_message_id):
        pass
    
    @abstractclassmethod
    def get_thread_messages_direct_id(self, direct_message_id):
        pass
    
    @abstractclassmethod
    def get_all_thread_messages(self):
        pass
    