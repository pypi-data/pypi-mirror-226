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
import Pyro4

import traceback
#Pyro4.config.COMMTIMEOUT = 4 #globally (for all Pyro network related operations) by setting the timeout config item:
#Pyro4.config.MAX_RETRIES = 2
try:
  helloSerObj = Pyro4.Proxy("PYRO:hello.service@0.0.0.0:8345")

  #helloSerObj = Pyro4.Proxy("PYRO:cbc.4c35c3e7-9166-36e8-9ff4-626feb94f5de.helloservice@0.0.0.0:8345")
  #helloSerObj = Pyro4.Proxy("PYRO:cbc.4c35c3e7-9166-36e8-9ff4-626feb94f5de.haservice@10.20.63.50:8344")
  helloSerObj._pyroTimeout = 10 #sec, per-proxy basis by setting the timeout property on the proxy
  #helloSerObj._pyroMaxRetries = 3

  response = helloSerObj.getHelloResponse()

  print response
except Pyro4.errors.TimeoutError as ex:
  """A call could not be completed within the set timeout period,
    or the network caused a timeout.
  """
  print "[Timedout]:Error:"+str(ex)  #Error:receiving: timeout
  traceback.print_stack()
except Pyro4.errors.ConnectionClosedError as ex:
  """The connection was unexpectedly closed."""
  print "[COnnectionClosed]:Error:"+str(ex)  #[COnnectionClosed]:Error:receiving: not enough data
  traceback.print_stack()  
  print "Reconnecting..."
  helloSerObj._pyroReconnect()
except Pyro4.errors.CommunicationError as ex:
  """errors related to network communication problems."""
  #helloSerObj = Pyro4.Proxy("PYRO:hello.service1@0.0.0.0:8345")
  print "[CommunicationError]:Error:"+str(ex)  #[CommunicationError]:Error:connection rejected, reason: unknown object

  #helloSerObj = Pyro4.Proxy("PYRO:hello.service@0.0.0.1:8345")  [CommunicationError]:Error:cannot connect: [Errno 22] Invalid argument

  #helloSerObj = Pyro4.Proxy("PYRO:hello.service@0.0.0.0:8346")  [CommunicationError]:Error:cannot connect: [Errno 111] Connection refused

  #[CommunicationError]:Error:invalid data or unsupported protocol version
  traceback.print_stack()

    


