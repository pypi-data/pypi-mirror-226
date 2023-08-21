# https://www.programiz.com/python-programming/class
# https://www.programiz.com/python-programming/closure
class Celcious:
  def __init__(self, temp):
     self._temp = temp

  @property
  def temprature(self):
    print("Getting temprature")
    return self._temp

  @temprature.setter
  def temprature(self, value):
    print("Setting temprature")
    if value < -1:
       raise ValueError("error not allowed")
    else:
      self._temp=value


if __name__ == '__main__':
   c = Celcious(10)
   c.temprature=13 # will call the validation
   print(c.temprature)
   print(c._temp)
   c._temp = 15 # will not call the validation
