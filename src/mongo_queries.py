import json
from pymongo import MongoClient


class MongoSearch():
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['slack_database']
        
    # pick a random user
    def randomUsersIds(self, count:int = 1) -> list:
        return [i['user_id'] for i in self.db.user_col.aggregate([{'$sample':{'size': count}}])]
    
    # pick a random workspace
    def randomWorkspaceIds(self, count:int = 1) -> list:
        return [i['_id'] for i in self.db.workspace_col.aggregate([{'$sample':{'size': count}}])]

    # find all workspaces a user is in
    def workspaceByUser(self, user_id: int) -> list:
        return [i['name'] for i in self.db.workspace_col.find({'members':user_id})]

    # find all messages in direct channel between two users
    # will return empty list if no direct channel between two users exists
    def dirChannelMessages(self, user_id_1: int, user_id_2: int):
        return [i['messages'] for i in self.db.direct_col.find({'member_ids':{'$all':[user_id_1, user_id_2]}})]

    # find names of all users in a workspace by workspace_id
    # TODO: This is returns username, spark version returns user_id
    def usersInWorkspace(self, workspace_id)->list:
        user_ids = [i['members'] for i in self.db.workspace_col.find({'_id':workspace_id})][0]
        usernames = []
        for user_id in user_ids:
            user =  self.db.user_col.find_one({'user_id': user_id})
            usernames.append(user['name'])
        return usernames
    
    # find all available channels in a random workspace
    # NOTE: returns error NoneType Subscriptable
    def channelNamesInRandomWorkspace(self)->list:
        workspaces = [i for i in self.db.workspace_col.aggregate([{'$sample':{'size': 1}}])]
        workspace_id = workspaces[0]['_id']
        channel_ids = [i['channels'] for i in self.db.workspace_col.find({'_id':workspace_id})][0]
        channel_names = []
        for channel_id in channel_ids:
            channel =  self.db.user_col.find_one({'channel_id': channel_id})
            channel_names.append(channel['name'])
        return channel_names

    # find names of all available channels in a workspace
    def channelNamesInWorkspace(self, workspace_id)->list:
        channels = [i['channels'] for i in self.db.workspace_col.find({'_id':workspace_id})][0]
        channel_names = [names for names, messages in channels.items()]
        return channel_names
    
    # find the channels in a workspace that are private
    # TODO: Fix channel settings in workspace
    # TODO: Fix this function
    # def privateChannelsInWorkspace(self, workspace_id)->list:
    #     channel_names = [i['channels'] for i in self.db.workspace_col.find({'_id':workspace_id})][0]
    #     private_channels = []
    #     for channel_name in channel_names:
    #         channel =  self.db.user_col.find_one({'private': true})       
    #         private_channels.append(channel['private'])
    #     return private_channels


def main():
    
    MG = MongoSearch()
    user_ids = MG.randomUsersIds(10)
    print(MG.workspaceByUser(user_ids[0]))
    print(MG.dirChannelMessages(user_ids[0], user_ids[1]))
    workspace_id = MG.randomWorkspaceIds()[0]
    print(MG.usersInWorkspace(workspace_id))
    print(MG.channelNamesInWorkspace(workspace_id))
    # print(MG.privateChannelsInWorkspace(workspace_id))
    
    

if __name__ == '__main__':
    main()