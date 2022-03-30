class Workspace:
    def __init__(self, name: str = None, workspace_id: int = None):
        #PK
        self.workspace_id = workspace_id
        
        self.name = name
        self.members = set()
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.channels = set()