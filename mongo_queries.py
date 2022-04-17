import json
from pymongo import MongoClient
# client = MongoClient("mongodb://localhost:27017/")
# db = client['slack_database']


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

    # find names of all users in a random workspace
    # THIS ONE IS RANDOM
    def userNamesInRandomWorkspace(self)->list:
        workspaces = [i for i in self.db.workspace_col.aggregate([{'$sample':{'size': 1}}])]
        workspace_id = workspaces[0]['_id']
        user_ids = [i['members'] for i in self.db.workspace_col.find({'_id':workspace_id})][0]
        usernames = []
        for user_id in user_ids:
            user =  self.db.user_col.find_one({'user_id': user_id})
            usernames.append(user['name'])
        return usernames


    # find names of all users in a workspace by workspace_id
    def usersInWorkspace(self, workspace_id)->list:
        user_ids = [i['members'] for i in self.db.workspace_col.find({'_id':workspace_id})][0]
        usernames = []
        for user_id in user_ids:
            user =  self.db.user_col.find_one({'user_id': user_id})
            usernames.append(user['name'])
        return usernames
    
    # pull all messages from a channel in workspace given channel _id

    # pull all messages in channel in a workspace posted by certain user by user_id
    
    

    


def main():
    MG = MongoSearch()
    user_ids = MG.randomUsersIds(10)
    print(MG.workspaceByUser(user_ids[0]))
    print(MG.dirChannelMessages(user_ids[0], user_ids[1]))
    
    workspace_id = MG.randomWorkspaceIds()[0]
    print(MG.usersInWorkspace(workspace_id))
    

if __name__ == '__main__':
    main()