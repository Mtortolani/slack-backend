from models import user
from models import channel



r = redis.Redis(host='localhost', port=6379, db=0)
r.set('users','this is a test from python')
res = r.get('test')



        


