import Queue
import threading
import multiprocessing
import subprocess

q = Queue.Queue()
for i in range(30): #put 30 tasks in the queue
    q.put(i)

def worker():
    while True:
        item = q.get()
        #execute a task: call a shell program and wait until it completes
        subprocess.call("echo "+str(item), shell=True) 
        q.task_done()

cpus=multiprocessing.cpu_count() #detect number of cores
print("Creating %d threads" % cpus)
for i in range(cpus):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()

q.join() #block until all tasks are done


"""
Usage of Deamon thread:
Lets say you are making some kind of dashboard widget. As part of this,
 you want it to display the unread message count in your email box. So you make a little thread that will:

Connect to the mail server and ask how many unread messages you have.
Signal the GUI with the updated count.
Sleep for a little while.
When your widget starts up, it would create this thread, designate it a daemon,
 and start it. Because its a daemon, you dont have to think about it;
  when your widget exits, the thread will stop automatically.
"""