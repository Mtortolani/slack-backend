from models.message import Message

class User:
    def __init__(self, username: str, user_id: int):
        #PK
        self.user_id = user_id
        #Attributes
        self.username = username
        self.profilePicture = 'Default Image'
        self.channels = set()
        self.directChannels = set()
        self.settings = {} #{'brightness':0.80, '}
        self.friends = set()
        self.blocked = set()
        

    
    #id
    def getId(self):
        return self.user_id
    
    #username 
    def __str__(self):
        return f'Username: {self.username}, id: {self.user_id}'
    
    #profile picture
    def getProfilePicture(self):
        return
    def setProfilePicture(self, image):
        if image == None:
            self.delProfilePicture()
        else:
            self.profilePicture = image
    def delProfilePicture(self):
        self.profilePicture = None
            
    #channels
    def joinChannel(self, channel_id: str):
        self.channels.add(channel_id)
    def leaveChannel(self, channel_id:str):
        self.channels.discard(channel_id)

        
    def postMessage(self, message: Message, channel_id: str):
        pass
