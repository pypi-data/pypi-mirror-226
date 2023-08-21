import datetime,time
from random import randint
from opcua import Server

s = Server()
url = "opc.tcp://10.242.143.74:4840"
s.set_endpoint(url)
namespace = "opc_server_simulator"

addr_space = s.register_namespace(namespace)
node = s.get_objects_node()
param = node.add_object(addr_space, "Parameter")
temp = param.add_variable(addr_space, "Temprature", 0)
print(dir(node))
temp.set_writable()
print("Server started at %s", url)
while True:
  t = randint(10, 50)
  print(t)
  temp.set_value(t)
  time.sleep(2)
