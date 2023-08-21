import logging
import os
import sys
import uuid

logging.basicConfig(level=logging.ERROR)

self_dir = os.path.abspath(os.path.dirname(__file__))
top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir,
                                       os.pardir))
sys.path.insert(0, top_dir)
sys.path.insert(0, self_dir)

from taskflow import engines
from taskflow.patterns import linear_flow
from taskflow import task
import time

# INTRO: This example shows how a task (in a linear/serial workflow) can
# produce an output that can be then consumed/used by a downstream task.


class TaskA(task.Task):
    default_provides = 'uuid'

    def execute(self):
        print("Executing task: '%s'" % (self.name))
        time.sleep(1)
        result = uuid.uuid4()
        print("Task: '%s' completed" % (self.name))
        return result


class TaskB(task.Task):
    def execute(self, uuid):
        print("Executing task: '%s'" % (self.name))
        print("Got input '%s'" % (uuid))


print("Constructing...")
wf = linear_flow.Flow("pass-from-to")
wf.add(TaskA('taskA'), TaskB('taskB'))   # Task B Will get the input from taskA

print("Loading...")
e = engines.load(wf)

print("Compiling...")
e.compile()

print("Preparing...")
e.prepare()

print("Running...")
e.run()

print("Done...")