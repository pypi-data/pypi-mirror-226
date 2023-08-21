class Emp:
   def __init__(self, name):
       self.name = name

count = 1
params = {}

class ObjCount:
  

   def __init__(self, name): 
      global params 
      global count  
      params.update({count: Emp(name)})  
        
      count +=1

   def display(self, cam_sn):
      print (params.get(cam_sn).name)
   

if __name__ == '__main__':
    e1 = ObjCount("Aafak")
    e2 = ObjCount("Aman")
   
    e1.display(2) 
       
