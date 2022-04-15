import time
import matplotlib.pyplot as plt

run_times = []

# for i in range(20):
#     start_time = time.process_time()
#     time.sleep(1)
#     # print(time.process_time() - start_time)
#     # print(start_time)
#     run_times.append(time.process_time() - start_time)

for i in range(10):
    start_time = time.time()
    time.sleep(1)
    print('running')
    # print(time.process_time() - start_time)
    # print(start_time)
    run_times.append(time.time() - start_time)

print(run_times)
plt.hist(run_times)
plt.show()