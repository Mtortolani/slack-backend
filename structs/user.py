from structs.message import Message



class User:
    def __init__(self, username: str, user_id: str =None):
        #PK
        self.user_id = user_id
        #Attributes
        self.username = username
        self.profilePicture = 'Default Image'
        self.channels = set()
        self.settings = {} #{'brightness':0.80, '}
        self.friends = set()
        self.blocked = set()
        
    def __str__(self):
        return str(self.username)
    
    
    
    def setProfilePicture(self, image):
        
        if image == None:
            self.profilePicture = 'Default Image'
        else:
            self.profilePicture = image
            
    
    def joinChannel(self, channel_id: str):
        self.channels.add(channel_id)
        
    def leaveChannel(self, channel_id:str):
        self.channels.discard(channel_id)

        
    def postMessage(self, message: Message, channel_id: str):
        pass
