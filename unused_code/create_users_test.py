from typing import Sized
import redis

import random
import string

from models.user import User
from models.channel import Channel

# Setup Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

def generate_random_string(size: int=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))

def generate_random_message():
    words = [generate_random_string() for i in range(random.randint(3,10))]
    return ' '.join(words)

# def generate_random_users(count: int=10):
#     # Get the current id counter from redis
#     id = int(r.get('next_user_id'))
#     id = 0 #TODO: check why do we reset to 0?

#     users = []
#     for i in range(count):
#         # Randomly generate a username of length 10 (letters and numbers)
#         username = generate_random_string()
#         user = User(username, id+i)
#         users.append(user)

#     # Increment user id counter in redis by the number of users created
#     r.set('next_user_id', id+count)

#     return users

# def generate_random_connections(count: int=5):
#     # list of all users (ids)
#     users = r.get('users')
#     for user in users:
#         for i in range(count):
#             # Operation to generate relationship
#             r.set()

def generate_random_data(users: int=10, workspaces: int=2, channels: int=3, direct_channels: int=1, channel_messages: int=5, direct_messages: int=2):
    '''
    Creates a database with the given number of users, workspaces, channels in each workspace, direct channels created by each user, messages by each user in channels,
    and messages by each user in direct channels.
    '''
    # Clear all previous data
    r.flushall()
    # Set id counters
    r.set('next_user_id', 0)
    r.set('next_workspace_id', 0)
    r.set('next_channel_id', 0)
    r.set('next_direct_channel_id', 0)
    r.set('next_message_id', 0)

    # Create workspaces
    for _ in range(workspaces):
        ws_id = int(r.get("next_workspace_id"))
        # Increment id counter
        r.incr('next_workspace_id')

        if _ % 2 == 0:
            workspace_user_list = list(range(0, users//2 + 1))
        else:
            workspace_user_list = list(range(users//2 - 1, users))

        # # Randomly generate users of this workspace
        # user_list = random.sample(range(users), users//2)
        for ws_user in workspace_user_list:
            r.lpush(f'workspace_{ws_id}_users', ws_user)
            # Add workspace to user's list
            r.lpush(f'user_{ws_user}_workspaces', ws_id)

        # Randomly generate channels in this workspace and populate with users
        for _ in range(channels):
            channel_id = int(r.get('next_channel_id'))
            # Increment id counter
            r.incr('next_channel_id')

            # Add channel to workspace
            r.lpush(f'workspace_{ws_id}_channels', channel_id)

            if _ % 2 == 0:
                channel_user_list = workspace_user_list[:len(workspace_user_list)//2 + 1]
            else:
                channel_user_list = workspace_user_list[len(workspace_user_list)//2 - 1:]

            for channel_user in channel_user_list:
                r.lpush(f'channel_{channel_id}_users', channel_user)
                # Add channel to user's list
                r.lpush(f'user_{channel_user}_channels', channel_id)

    # Generate random channel messages
    for user in range(users):
        for m in range(channel_messages):
            message_id = int(r.get('next_message_id'))
            # Increment id counter
            r.incr('next_message_id')
            r.hset(f'message_{message_id}', 'sender', user)
            r.hset(f'message_{message_id}', 'message', generate_random_message())
            # Add message to user's list and random user's channel list
            # r.lpush(f'user_{user}_messages', message_id)
            user_channels = [int(channel_id) for channel_id in r.lrange(f'user_{user}_channels', 0, -1)]
            r.lpush(f'channel_{random.sample(user_channels, 1)[0]}_messages', message_id)

    # Create users with their direct channels
    for _ in range(users):
        user_id = int(r.get('next_user_id'))
        # Increment id counter
        r.incr('next_user_id')

        dc = random.sample(range(users), direct_channels+1)
        count = 0
        for dc_user in dc:
            # If given number of direct channels have been created
            if count == direct_channels:
                break
            # If the user isn't creating a direct channel with themselves
            if user_id != dc_user:
                # Save each other's user id
                r.lpush(f'user_{user_id}_dcs', dc_user)
                r.lpush(f'user_{dc_user}_dcs', user_id)
                # # Create direct channel and create messages
                dc_id = int(r.get('next_direct_channel_id'))
                # Increment id counter
                r.incr('next_direct_channel_id')
                message_id = int(r.get('next_message_id'))
                # Increment id counter
                r.incr('next_message_id')
                r.hset(f'message_{message_id}', 'sender', user_id)
                r.hset(f'message_{message_id}', 'message', generate_random_message())
                # Add message to direct channel's list
                r.lpush(f'dc_{dc_id}_messages', message_id)
                count+=1


# '''
# Simple test to check if server is functioning
# '''
# r.flushall()
# r.set('foo', 'bar')
# print(f"Result: {r.get('foo')}")
# print(r.keys())

def main():
    '''
    Simple test to check if server is functioning
    '''
    r.flushdb()
    r.set('foo', 'bar')
    print(f"Result: {r.get('foo')}")
    print(r.keys())

    r.set('next_user_id', 0)

    '''
    Testing random user generation function
    '''
    # for user in generate_random_users():
    #     print(user)

    # r.set('next_user_id', 0)
    # print(r.get('next_user_id'))
    # a()

    print(generate_random_message())

    generate_random_data()

if __name__ == '__main__':
    main()
