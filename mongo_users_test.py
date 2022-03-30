from email import generator
from os import listdir
from os.path import isfile, join
import numpy as np
import random
import string
from pymongo import MongoClient
from models.user import User
from models.channel import *
from models.workspace import Workspace
import redis

# Setup Mongo client
class MongoDatabase:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['slack_database']
        self.user_col = self.db['user_col']
        self.direct_col = self.db['direct_col']
        self.workspace_col = self.db['workspace_col']


class Generator:
    def __init__(self):
        self.mongo = MongoDatabase()
        
    def generate_random_string(self, size: int=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))

    def generate_random_number(self, size: int=9):
        return random.randint(1, 10**size)

    def generate_random_message(self):
        words = [self.generate_random_string() for i in range(random.randint(3,10))]
        return ' '.join(words)

    def generate_random_user(self):
        username = self.generate_random_string()
        user = User(username)
        return user
    
    def generate_random_channel(self):
        channel = Channel()
        return channel
    
    def generate_random_direct_channel(self, user_1: User, user_2: User):
        dc = DirectChannel(user_1, user_2)
        return dc

    def generate_random_workspace(self):
        workspace_name = self.generate_random_string()
        space = Workspace(workspace_name)
        return space
        
    
        

# def generate_random_connection():
#     # list of all users (ids)
#     users = mongo.user_col.find()
#     for user in users:
#         for i in range(count):
#             # TODO: Operation to generate relationship
#             pass #
    
    
def random_data_test(user_count: int=100, workspace_count: int=5, channel_count: int=10,
                     direct_channel_count: int=20, message_count: int=50):
    '''
    Creates a database with the given number of users, workspaces, channels in each workspace, direct channels for each user, and messages by each user
    '''
    g = Generator()
    mongo = MongoDatabase()
    # make users
    for _ in range(user_count):
        user = g.generate_random_user()
        mongo.user_col.insert_one({
            'user_id': user.user_id,
            'username': user.username})
        
    # make direct channels with messages
    for _ in range(direct_channel_count):
        user_pair = [i for i in mongo.user_col.aggregate([{'$sample':{'size':2}}])]
        dc = g.generate_random_direct_channel(user_pair[0], user_pair[1])
        dc.messages = [g.generate_random_message() for _ in range(message_count)]
        mongo.direct_col.insert_one({'member_ids': dc.member_ids, 
                                     'messages': dc.messages})

    # make workspaces with members and channels and messages
    for _ in range(workspace_count):
        workspace = g.generate_random_workspace()
        workspace.member_ids = [i['user_id'] for i in mongo.user_col.aggregate([{'$sample':{'size':7}}])]
        workspace.channels = [g.generate_random_channel() for _ in range(channel_count)]
        for channel in workspace.channels:
            channel.name = g.generate_random_string()
            channel.messages = [g.generate_random_message() for _ in range(message_count)]
        
        workspace_dict = {'members':workspace.member_ids,
                          'channels': {channel.name: channel.messages for channel in workspace.channels}}
        mongo.workspace_col.insert_one(workspace_dict)


def main():
    mongo = MongoDatabase()
    mongo.client.drop_database('slack_database')

    random_data_test()

if __name__ == '__main__':
    main()