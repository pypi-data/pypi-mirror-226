from taskflow.patterns import linear_flow
from taskflow import task
from taskflow import engines
from taskflow import retry
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
    flow = linear_flow.Flow('CalculatorFlow')\
        .add(CalculateTask('AddTask', 10, 20, inject={'action': 'sum'}))\
        .add(CalculateTask('SubtractTask',100, 200, inject={'action': 'sub'}))\
        .add(CalculateTask('MultiplyTask',1000, 2000, inject={'action': 'mul'}))

    # e = engines.load(flow, engine='serial')
    # e.run()

    flow = linear_flow.Flow('MyPrinterFlow') \
        .add(PrinterTask('PythonPrinter', inject={'language': "Python", 'author': 'Romso'})) \
        .add(PrinterTask('JavaPrinter', inject={'language': "Java", 'author': 'Gosling'})) \
        .add(PrinterTask('CPrinter', inject={'language': "C", 'author': 'Kantekar'}))

    # engines.run(flow)  # Working

    e = engines.load(flow, executor='threaded', engine='parallel',
                     max_workers=1)
    e.run()


