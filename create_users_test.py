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

def generate_random_users(count: int=10):
    # Get the current id counter from redis
    id = int(r.get('next_user_id'))
    id = 0

    users = []
    for i in range(count):
        # Randomly generate a username of length 10 (letters and numbers)
        username = generate_random_string()
        user = User(username, id+i)
        users.append(user)

    # Increment user id counter in redis by the number of users created
    r.set('next_user_id', id+count)

    return users

def generate_random_connections(count: int=5):
    # list of all users (ids)
    users = r.get('users')
    for user in users:
        for i in range(count):
            # Operation to generate relationship
            r.set()

def generate_random_data(users: int=10, workspaces: int=2, channels: int=3, direct_channels: int=1):
    # Clear all previous data
    r.flushall()
    # Set id counters
    r.set('next_user_id', 0)
    r.set('next_workspace_id', 0)
    r.set('next_channel_id', 0)
    # r.set('next_direct_channel_id', 0)
    r.set('next_message_id', 0)

    # Create workspaces
    for _ in range(workspaces):
        ws_id = r.get("next_workspace_id")

        # Randomly generate users in this workspace
        user_list = random.sample(range(users), users//2)
        for usr in user_list:
            r.lpush(f'workspace_{ws_id}_users', usr)

        # Increment id counter
        r.incr('next_workspace_id')


    pass


'''
Simple test to check if server is functioning
'''
r.flushall()
r.set('foo', 'bar')
print(f"Result: {r.get('foo')}")
print(r.keys())

r.set('next_user_id', 0)

'''
Testing random user generation function
'''
for user in generate_random_users():
    print(user)

# r.set('next_user_id', 0)
# print(r.get('next_user_id'))
# a()

print(generate_random_message())

generate_random_data()
