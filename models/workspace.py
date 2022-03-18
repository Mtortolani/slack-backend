class Workspace:
    def __init__(self, name: str = None):
        #PK
        self.corkspace_id = None
        
        self.name = name
        self.members = set()
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.channels = set()