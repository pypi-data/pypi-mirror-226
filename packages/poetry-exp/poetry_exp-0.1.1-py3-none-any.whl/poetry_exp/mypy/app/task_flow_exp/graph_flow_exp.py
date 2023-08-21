from taskflow.patterns import graph_flow
from taskflow import task
from taskflow import engines
from taskflow import retry
from datetime import datetime
import time

class PrinterTask(task.Task):
    def __init__(self, name, show_name=True, inject=None):
        super(PrinterTask, self).__init__(name, inject=inject)
        self._show_name = show_name

    def execute(self, language, author):
        for i in range(10):
            if self._show_name:
                print("[%s]: Language: %s, Author: %s" % (self.name, language, author))
            else:
                print("Language: %s, Author: %s" % (language, author))
            time.sleep(1)


class CalculateTask(task.Task):
    def __init__(self, name, num1, num2, show_name=True, inject=None):
        super(CalculateTask, self).__init__(name, inject=inject)
        self._show_name = show_name
        self.num1 = num1
        self.num2 = num2

    def execute(self, action, *args, **kwargs):
        print('args: {0}'.format(args))
        print('kwargs: {0}'.format(kwargs))
        if action == 'sum':
            sum = self.num1 + self.num2
            print('{0} + {1} = {2}'.format(self.num1, self.num2, sum))
        elif action == 'sub':
            sum = self.num1 - self.num2
            print('{0} - {1} = {2}'.format(self.num1, self.num2, sum))
        if action == 'mul':
            sum = self.num1 * self.num2
            print('{0} * {1} = {2}'.format(self.num1, self.num2, sum))


if __name__ == '__main__':
    flow = graph_flow.Flow('CalculatorFlow')\
        .add(CalculateTask('AddTask', 10, 20, inject={'action': 'sum'}))\
        .add(CalculateTask('SubtractTask',100, 200, inject={'action': 'sub'}))\
        .add(CalculateTask('MultiplyTask',1000, 2000, inject={'action': 'mul'}))

    # e = engines.load(flow, engine='serial')
    # e.run()

    flow = graph_flow.Flow('MyPrinterFlow') \
        .add(PrinterTask('PythonPrinter', inject={'language': "Python", 'author': 'Romso'})) \
        .add(PrinterTask('JavaPrinter', inject={'language': "Java", 'author': 'Gosling'})) \
        .add(PrinterTask('CPrinter', inject={'language': "C", 'author': 'Kantekar'})) \
        .add(PrinterTask('CPrinter2', inject={'language': "C2", 'author': 'Kantekar'})) \
        .add(PrinterTask('CPrinter3', inject={'language': "C3", 'author': 'Kantekar'})) \
        .add(PrinterTask('CPrinter4', inject={'language': "C4", 'author': 'Kantekar'})) \
        .add(PrinterTask('CPrinter5', inject={'language': "C5", 'author': 'Kantekar'})) \


    # executor: ['greenthreads', 'greenthread', 'greenthreaded', 'threads', 'thread', 'threaded', 'process', 'processes']

    # e = engines.load(flow)  # 70 sec
    # e = engines.load(flow, executor='processes', engine='parallel', max_workers=7) # 16 sec
    # e = engines.load(flow, executor='threaded', engine='parallel', max_workers=7)  # 10 sec
    # e = engines.load(flow, executor='process', engine='parallel', max_workers=7)  # 15 sec
    e = engines.load(flow, executor='greenthreads', engine='parallel', max_workers=7)  # 70 sec


    t1 = datetime.now()
    e.run()
    t2 = datetime.now()
    delta = t2-t1
    print('Time taken: {0}'.format(delta.seconds))


"""
Engine type: 
1. 'serial': Runs all tasks on a single thread – the same thread run() is called from. This engine is used by default.
2. 'parallel': A parallel engine schedules tasks onto different threads/processes to allow for 
               running non-dependent tasks simultaneously. See the documentation of ParallelActionEngine for
               supported arguments that can be used to construct a parallel engine that runs using your desired
               execution model.
               
3. 'worker-based' or 'workers': this engine is significantly more complicated (and different) then the others
      see here https://docs.openstack.org/taskflow/ocata/workers.html
      flow = lf.Flow('simple-linear').add(...)
      eng = taskflow.engines.load(flow, engine='worker-based',
                            url='amqp://guest:guest@localhost:5672//',
                            exchange='test-exchange',
                            topics=['topic1', 'topic2'])
      eng.run()
      
      from taskflow.engines.worker_based import worker as w
      config = {
        'url': 'amqp://guest:guest@localhost:5672//',
        'exchange': 'test-exchange',
        'topic': 'test-tasks',
        'tasks': ['tasks:TestTask1', 'tasks:TestTask2'],
      }
      worker = w.Worker(**config)
      worker.run()

Executor type:

String (case insensitive)	Executor used
process            	       ParallelProcessTaskExecutor
processes	               ParallelProcessTaskExecutor
thread	                   ParallelThreadTaskExecutor
threaded	               ParallelThreadTaskExecutor
threads	                   ParallelThreadTaskExecutor
greenthread	               ParallelThreadTaskExecutor(greened version)
greedthreaded	           ParallelThreadTaskExecutor(greened version)
greenthreads	           ParallelThreadTaskExecutor(greened version)


Sharing an executor between engine instances provides better scalability by reducing thread/process
creation and teardown as well as by reusing existing pools (which is a good practice in general).
"""