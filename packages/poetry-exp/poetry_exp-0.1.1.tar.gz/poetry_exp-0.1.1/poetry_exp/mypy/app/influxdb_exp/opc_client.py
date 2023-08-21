from opcua import Client

url = "opc.tcp://10.242.143.74:4840"
client = Client(url)
client.connect()
print("client connected")
