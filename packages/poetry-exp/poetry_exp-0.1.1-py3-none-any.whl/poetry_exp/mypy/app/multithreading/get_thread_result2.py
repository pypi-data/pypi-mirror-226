from threading import Thread
import time

# Approach2:
result = {}


class Parent(Thread):

    def run(self):
        print 'Running Parent Thread...'
        c1 = Child1()
        c2 = Child2()
        c1.start()
        c2.start()
        c1.join()
        c2.join()
        print 'End Parent Thread...'

        if result['child1_result'] and result['child2_result']:
            result['parent_result'] = True
        else:
            result['parent_result'] = False


class Child1(Thread):
    def run(self):
        print 'Running Child1 Thread...'
        time.sleep(3)
        print 'End Chilld1 Thread...'
        result['child2_result'] = True


class Child2(Thread):
    def run(self):
        print 'Running Child2 Thread...'
        time.sleep(3)
        print 'End Chilld2 Thread...'
        result['child1_result'] = True


if __name__ == '__main__':

  p = Parent()
  p.start()
  p.join()

  print result['parent_result']