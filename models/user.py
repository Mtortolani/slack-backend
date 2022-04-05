import random
from models.message import Message
from models.settings import UserSetting

class User:
    def __init__(self, username: str):
        #PK
        self.user_id = random.randint(10**9,10**10)
        #Attributes
        self.username = username
        self.profilePicture = 'Default Image'
        self.channels = set()
        self.directChannels = set()
        self.settings = UserSetting() #{'brightness':0.80, '}
        self.friends = set()
        self.blocked = set()
        

