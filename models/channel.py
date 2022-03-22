
class Channel:
    def __init__(self, workspace_id: str):
        #PK
        self.channel_id = None
        #FK
        self.workspace_id = None
        #Attributes
        self.directChannel = None
        self.private = True
        self.banned = set()
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}

    
    #id
    def getId(self):
        return self.channel_id
    def setId(self, id):
        self.channel_id = id
    
    #direct
    def isDirect(self):
        return self.directChannel
    
    #private
    def isPrivate(self):
        return self.private
    def makePrivate(self):
        self.private = True
    def makePublic(self):
        self.private = False
    
    #banned
    def getBanned(self):
        return self.banned
    def banUser(self, userId):
        self.banned.add(userId)
    def unBanUser(self, userId):
        self.banned.discard(userId)
        
    #roles
    def getRoles(self):
        return self.roles
    def addRole(self, role, user):
        if not role in self.roles:
            self.roles[role] = user
        else:
            self.roles[role].append(user)