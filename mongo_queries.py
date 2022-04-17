import json
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['slack_database']



# pick a random user
def randomUsersIds(count:int = 1) -> list:
    return [i['user_id'] for i in db.user_col.aggregate([{'$sample':{'size': count}}])]

# find all workspaces a user is in
def workspaceByUser(user_id: int) -> list:
    return [i['name'] for i in db.workspace_col.find({'members':user_id})]

# find all messages in direct channel between two users
# will return empty list if no direct channel between two users exists
def dirChannelMessages(user_id_1: int, user_id_2: int):
    return [i['messages'] for i in db.direct_col.find({'member_ids':{'$all':[user_id_1, user_id_2]}})]

# find names of all users in a workspace
def userNamesInRandomWorkspace()->list:
    workspaces = [i for i in db.workspace_col.aggregate([{'$sample':{'size': 1}}])]
    workspace_id = workspaces[0]['_id']
    user_ids = [i['members'] for i in db.workspace_col.find({'_id':workspace_id})][0]
    usernames = []
    for user_id in user_ids:
        user =  db.user_col.find_one({'user_id': user_id})
        usernames.append(user['name'])
    return usernames


def main():
    user_ids = randomUsersIds(10)
    print(workspaceByUser(user_ids[0]))
    print(dirChannelMessages(user_ids[0], user_ids[1]))
    print(userNamesInRandomWorkspace())
    

if __name__ == '__main__':
    main()