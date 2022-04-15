from re import S
import time

start_time = time.process_time()
for _ in range(200000):
    print(_)
print(time.process_time() - start_time)
print(start_time)