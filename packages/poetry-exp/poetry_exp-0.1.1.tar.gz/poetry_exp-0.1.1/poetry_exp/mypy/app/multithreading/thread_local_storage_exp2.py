
import threading
from threading import Thread, current_thread
import os, time


def fun1(task_id):
    thread_local = threading.local()
    thread_local.context = {
        'task_id': task_id
    }
    print(f'current_thread: {thread_local.context}')

    for i in range(10):
        time.sleep(2)
        print(f"[{task_id}], context: {thread_local.context}")


if __name__ == '__main__':
    threads = []
    for i in range(5):
        t1 = threading.Thread(target=fun1, args=("task-" + str(i),))
        threads.append(t1)
        t1.start()
    for t in threads:
        t.join()


"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/multithreading/thread_local_storage_exp.py"
Thread: Thread-1(172580) initialized with task_id: task-0
Thread: Thread-2(172580) initialized with task_id: task-1
Thread: Thread-3(172580) initialized with task_id: task-2
Thread: Thread-4(172580) initialized with task_id: task-3
Thread: Thread-5(172580) initialized with task_id: task-4
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-4]Executng thread: Thread-5, context: {'name': 'Thread-5', 'task_id': 'task-4'}
[task-1]Executng thread: Thread-2, context: {'name': 'Thread-2', 'task_id': 'task-1'}
[task-0]Executng thread: Thread-1, context: {'name': 'Thread-1', 'task_id': 'task-0'}
[task-2]Executng thread: Thread-3, context: {'name': 'Thread-3', 'task_id': 'task-2'}
[task-3]Executng thread: Thread-4, context: {'name': 'Thread-4', 'task_id': 'task-3'}

Process finished with exit code 0

"""