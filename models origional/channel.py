
class Channel:
    def __init__(self):
        #Attributes
        self.name = None
        self.private = False
        self.priaveMembers = None
        self.banned = set()
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.messages = []

    
    # #id
    # def getId(self):
    #     return self.channel_id
    # def setId(self, id):
    #     self.channel_id = id
    
    
    # #private
    # def isPrivate(self):
    #     return self.private
    # def makePrivate(self):
    #     self.private = True
    # def makePublic(self):
    #     self.private = False
    
    # #banned
    # def getBanned(self):
    #     return self.banned
    # def banUser(self, userId):
    #     self.banned.add(userId)
    # def unBanUser(self, userId):
    #     self.banned.discard(userId)
        
    # #roles
    # def getRoles(self):
    #     return self.roles
    # def addRole(self, role, user):
    #     if not role in self.roles:
    #         self.roles[role] = user
    #     else:
    #         self.roles[role].append(user)
            

class DirectChannel(Channel):
    def __init__(self, channel_id: int, user_id_1: str, user_id_2: str):
        super.__init__(channel_id, None)
        self.private = True
        self.privateMembers = set(user_id_1, user)
        