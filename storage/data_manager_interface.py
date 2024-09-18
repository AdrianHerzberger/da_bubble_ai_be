from abc import ABC, abstractclassmethod

class DataManagerInterface(ABC):
    @abstractclassmethod
    def create_user(self, user_email, user_name, user_passwor):
        pass
    
    
    @abstractclassmethod
    def get_user(self, user_name, user_password):
        pass