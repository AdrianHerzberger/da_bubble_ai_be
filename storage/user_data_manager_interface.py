from abc import ABC, abstractclassmethod

class UserDataManagerInterface(ABC):
    @abstractclassmethod
    def create_user(self, user_email, user_name, user_passwor):
        pass
    
    @abstractclassmethod
    def get_all_users(self):
        pass
    
    @abstractclassmethod
    def get_user(self, user_name, user_password):
        pass
    
    @abstractclassmethod
    def get_user_by_id(self, user_id):
        pass
    
    @abstractclassmethod
    def get_user_by_email(self, user_email):
        pass
    
    @abstractclassmethod
    def update_user_profile_picture(self, user_id, user_profile_picture_url):
        pass