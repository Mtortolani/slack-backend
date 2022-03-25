import redis
from models.user import User
from models.channel import Channel

# Setup Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

def generate_random_users(count: int=10) -> list(User):
    # Get the current id counter from redis
    id = int.from_bytes(r.get('next_user_id'))
    for i in range(count):
        pass
    return []


'''
Simple test to check if server is functioning
'''
r.flushall()
r.set('foo', 'bar')
print(f"Result: {r.get('foo')}")
print(r.keys())



        


