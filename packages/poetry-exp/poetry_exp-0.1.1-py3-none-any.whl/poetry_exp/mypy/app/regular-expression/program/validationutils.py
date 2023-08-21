import re

class ValidationUtils(object):

   def __init__(self):
     self.person_name_pattern = "^[a-zA-Z]*"
    
   def validatePersonName(self, name):
      return self.validate(self.person_name_pattern, name)


   def validate(self, patten, string):
     pat = re.compile(patten)
     matched = pat.match(string)
     if matched:
        return True
     else:
       return False

vu = ValidationUtils()

nameList = ["Abc", 'xyz123', '123pqr', ]
for name in nameList:
  print "is %s a valid name: %s" %(name ,vu.validatePersonName(name))
