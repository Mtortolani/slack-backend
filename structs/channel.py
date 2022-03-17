class Channel:
    def __init__(self, workspace_id: str):
        #PK
        self.channel_id = None
        #FK
        self.workspace_id = None
        
        self.isPrivate = True
        self.banned = set()
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.channels = set()