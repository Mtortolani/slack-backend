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
    
    def generate_random_direct_channel(self, n_messages: int = 10):
        user_pair = [i for i in self.mongo.user_col.aggregate([{'$sample':{'size':2}}])]
        dc = DirectChannel(user_pair[0], user_pair[1])
        dc.messages = [self.generate_random_message() for _ in range(n_messages)]
        return dc

    def generate_random_workspace(self, n_users: int = 10, n_channels: int = 10, n_msgs_per_chnl: int = 20):
        workspace_name = self.generate_random_string()
        workspace = Workspace(workspace_name)
        workspace.member_ids = [i['user_id'] for i in self.mongo.user_col.aggregate([{'$sample':{'size':n_users}}])]
        workspace.channels = [self.generate_random_channel() for _ in range(n_channels)]
        for channel in workspace.channels:
            channel.name = self.generate_random_string()
            channel.messages = [self.generate_random_message() for _ in range(n_msgs_per_chnl)]
        return workspace
        

    
    
def random_data_test(user_count: int=100, workspace_count: int=50, channel_count: int=10,
                     direct_channel_count: int=20, n_msgs_per_chnl: int=50):
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
        dc = g.generate_random_direct_channel(n_msgs_per_chnl)
        mongo.direct_col.insert_one({'member_ids': dc.member_ids, 
                                     'messages': dc.messages})

    # make workspaces with members and channels and messages
    for _ in range(workspace_count):
        workspace = g.generate_random_workspace(10, channel_count, n_msgs_per_chnl)
        mongo.workspace_col.insert_one({'members':workspace.member_ids,
                          'channels': {channel.name: channel.messages for channel in workspace.channels}})


def main():
    mongo = MongoDatabase()
    mongo.client.drop_database('slack_database')

    random_data_test()

if __name__ == '__main__':
    main()