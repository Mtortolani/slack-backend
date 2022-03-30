class Workspace:
    def __init__(self, name: str = None):
        #PK
        self.name = name
        self.members = []
        self.member_ids= []
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.channels = []
    
    
    #name
    def getName(self):
        return self.name
    def setName(self, name: str):
        self.name = name
        
    #members
    def getMembers(self):
        return self.members
    def addMembers(self, user_id: int):
        self.members.add(user_id)
    
    