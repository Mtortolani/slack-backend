import redis
from models.message import Message
from models.workspace import Workspace

M1 = Message('message content', 'author_id', 'channel_id')
print(M1)
print(M1.message_id)

W1 = Workspace('Workspace 1 Title')



m = Message('message content')
print(m)
print(m.message_id)


r = redis.Redis(host='localhost', port=6379, db=0)
r.set('test','this is a test from python')
res = r.get('test')

print(res)
print(type(res))
print(str(res)[0])

