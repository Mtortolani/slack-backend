from structs.message import Message
import redis

m = Message('whats up', '1224wiaer', 'eojeowq01', '12ej39')
print(m)
print(m.message_id)


r = redis.Redis(host='localhost', port=6379, db=0)
r.set('test','this is a test from python')
res = r.get('test')
print(res)
print(type(res))
print(str(res)[0])