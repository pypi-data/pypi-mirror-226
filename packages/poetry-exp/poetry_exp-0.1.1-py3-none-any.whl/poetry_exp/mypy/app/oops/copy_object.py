import copy

class Cont:
   def __init__(self, name):
        self.name = name

class PCB:

   def __init__(self,l, r, name):
      self.l = l
      self.r = r
      self.c = Cont(name)

   def display(self):
       print("l: "+str(self.l))
       print("r: "+str(self.r))
       print("Cont name: "+self.c.name)



if __name__ == '__main__':
    p1 = PCB(10, 12, "A")
    p2 = copy.copy(p1)
    p1.display()
    p2.display()
    p1.l=50  # will change only in p1
    p1.c.name='B'  # will change both, if want to change only in P1 not in p2 then use p2 = copy.deepcopy(p1)
    
    print('..............')
    p1.display()
    p2.display()

