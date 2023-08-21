#!/usr/bin/env python3
# countasync.py

import time

def count(task_name):
    print("Task: {0}, One".format(task_name))
    time.sleep(1)
    print("Task: {0}, Two".format(task_name))

def main():
    for i in range(1, 4):
      count("task"+str(i))


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")