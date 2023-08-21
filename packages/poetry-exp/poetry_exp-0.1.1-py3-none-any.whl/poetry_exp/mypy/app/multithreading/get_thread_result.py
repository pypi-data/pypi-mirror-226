from threading import Thread
import time


# Approach1:
class Parent(Thread):

    def run(self):
        print 'Running Parent Thread...'
        c1 = Child1()
        c2 = Child2()
        c1.start()
        c2.start()
        c1_result = c1.join()
        c2_result = c2.join()
        print 'End Parent Thread...'

        if c1_result and c2_result:
            self.result =  True
        else:
            self.result = False

    def join(self, timeout=None):
        Thread.join(self)
        return self.result


class Child1(Thread):
    def run(self):
        print 'Running Chilld1 Thread...'
        time.sleep(3)
        print 'End Chilld1 Thread...'
        self.result = True

    def join(self):
        Thread.join(self)
        return self.result


class Child2(Thread):
    def run(self):
        print 'Running Chilld2 Thread...'
        time.sleep(3)
        print 'End Chilld2 Thread...'
        self.result = False

    def join(self):
        Thread.join(self)
        return self.result


if __name__ == '__main__':

  p = Parent()
  p.start()
  print p.join()