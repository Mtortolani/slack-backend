from models.message import Message
from models.user import User
class Channel:
    def __init__(self):
        #Attributes
        self.private = False
        self.member_ids = []
        self.banned = []
        self.roles = {} #{owners:[user1], administrators:[user5, user8], etc}
        self.messages = []


class DirectChannel(Channel):
    def __init__(self, user_1: User, user_2: User):
        super().__init__()
        self.private = True
        self.member_ids = [user_1['user_id'], user_2['user_id']]
        