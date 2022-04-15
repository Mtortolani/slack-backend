from re import S
import time
import matplotlib.pyplot as plt

run_times = []

for i in range(50):
    start_time = time.process_time()
    for _ in range(10000):
        print(_)
    # print(time.process_time() - start_time)
    # print(start_time)
    run_times.append(time.process_time() - start_time)

print(run_times)
plt.hist(run_times)
plt.show()