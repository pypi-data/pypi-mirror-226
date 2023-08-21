import Pyro4
import time

class HelloService(object):

  def getHelloResponse(self):
    print "Processing hello response...."
    time.sleep(10)
    print "processed"
    return "Hello from server"

hsUri = "hello.service"
hs = HelloService()
try: 
  Pyro4.Daemon.serveSimple({hs:hsUri}, host="0.0.0.0", port=8345, ns=False)
except Pyro4.errors.NamingError as ex:
  """There was a problem related to the name server or object names.""" #Pyro4.Daemon.serveSimple({hs:hsUri}, "0.0.0.0", 8345, ns=True)
  print "[NamingError]: "+str(ex)  #[NamingError]: Failed to locate the nameserver
"""

root@aafak-HP-ProBook-4530s:~/aafak/python-demo/python-program/PYRO/program/helloService# pyro4-ns
Not starting broadcast server for localhost.
NS running on localhost:9090 (127.0.0.1)
Warning: HMAC key not set. Anyone can connect to this server!
URI = PYRO:Pyro.NameServer@localhost:9090


root@aafak-HP-ProBook-4530s:~/aafak/python-demo/python-program/PYRO/program# python helloResponseServer.py
Object <__main__.HelloService object at 0x2b385d0>:
    uri = PYRO:hello.service@0.0.0.0:8345
Pyro daemon running.

"""



