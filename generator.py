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
from models.settings import *
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
        name = self.generate_random_string()
        user = User(name)
        settings = UserSetting()
        settings.notifications = self.generate_notifications()
        settings.language = self.generate_random_language()
        settings.time_zone = self.generate_random_timezone()
        user.settings = settings
        return user
    
    def generate_random_channel(self):
        name = self.generate_random_string()
        channel = Channel(name)
        settings = ChannelSetting()
        settings.censored_words = [self.generate_random_string() for i in range(random.randint(3,10))]
        settings.archive = self.generate_random_archive()
        channel.settings = settings
        return channel
    
    def generate_random_direct_channel(self, n_messages: int = 10):
        user_pair = [i for i in self.mongo.user_col.aggregate([{'$sample':{'size':2}}])]
        dc = DirectChannel(user_pair[0], user_pair[1])
        dc.censored_words = [self.generate_random_string() for i in range(random.randint(3,10))]
        dc.archive = self.generate_random_archive()
        dc.messages = [self.generate_random_message() for _ in range(n_messages)]
        
        settings = ChannelSetting()
        settings.censored_words = [self.generate_random_string() for i in range(random.randint(3,10))]
        settings.archive = self.generate_random_archive()
        dc.settings = settings
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


        # For Settings
    def generate_random_language(self):
        language_list =  ["German","English","Spanish","French","Italian","Portuguese","Russian","Japanese","Chinese","Korean"]
        return random.choice(language_list)

    def generate_random_timezone(self):
        timezones = ['EST', 'CST', 'MST', 'PST', 'AST', 'AKST', 'HST']
        return random.choice(timezones)

    def generate_notifications(self):
        return bool(random.getrandbits(1))

    def generate_random_archive(self):
        return bool(random.getrandbits(1))


    
    
def random_data_test(user_count: int=1000, workspace_count: int=100, channel_count: int=5,
                     direct_channel_count: int=400, n_msgs_per_chnl: int=50):
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
            'name': user.name,
            'settings': {'notifications': user.settings.notifications,
                         'language': user.settings.language,
                         'time_zone': user.settings.time_zone}})
        
    # make direct channels with messages
    for _ in range(direct_channel_count):
        dc = g.generate_random_direct_channel(n_msgs_per_chnl)
        mongo.direct_col.insert_one({'member_ids': list(dc.member_ids), # NOTE: CHANGING FROM SET To LIST 
                                     'messages': dc.messages,
                                     'settings':{'censored_words': list(dc.settings.censored_words), # NOTE: CHANGING FROM SET To LIST
                                                 'archive': dc.settings.archive}})

    # make workspaces with members and channels and messages
    for _ in range(workspace_count):
        workspace = g.generate_random_workspace(10, channel_count, n_msgs_per_chnl)
        mongo.workspace_col.insert_one({'name':workspace.name,
                                        'members':workspace.member_ids,
                                        'channels': {channel.name: channel.messages for channel in workspace.channels},})
        # TODO: Inesrt settings into workspace channels

def main():
    mongo = MongoDatabase()
    mongo.client.drop_database('slack_database')

    random_data_test()

if __name__ == '__main__':
    main()