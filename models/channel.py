from django.forms import NullBooleanField


class Channel:
    def __init__(self, workspace_id: str):
        #PK
        self.channel_id = None
        #FK
        self.workspace_id = None
        #Attributes
        self.isDirect = None
        self.isPrivate = True
        self.banned = set()
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.channels = set()
    
    #id
    def getId(self):
        return self.channel_id
    def setId(self, id):
        self.channel_id = id
    
    #direct
    def isDirect(self):
        return self.isDirect
    
    #private
    def isPrivate(self):
        return self.isPrivate
    def makePrivate(self):
        self.isPrivate = True
    def makePublic(self):
        self.isPrivate = False
    
    #banned
    def getBanned(self):
        return self.banned
    def banUser(self, userId):
        self.banned.add(userId)
    def unBanUser(self, userId):
        self.banned.discard(userId)