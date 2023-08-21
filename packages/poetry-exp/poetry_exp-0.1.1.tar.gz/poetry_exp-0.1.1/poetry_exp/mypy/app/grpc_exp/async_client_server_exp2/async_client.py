"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""

import logging
import asyncio
import grpc

import helloworld_pb2
import helloworld_pb2_grpc

from client_handler import ClientHandler

global hw_channel

SERVER = 'localhost'
PORT = '50051'


class HelloWorldClient(ClientHandler):
    def __init__(self):
        global hw_channel
        hw_channel = None
        ClientHandler.__init__(
            self, SERVER, PORT)

    def make_channel(self):
        global hw_channel
        if not hw_channel:
            hw_channel = self.create_channel()
        else:
            raise Exception("create channel failed")
        return hw_channel

    async def greet(self, **kwargs):
        try:
            name = kwargs.get('name')
            global hw_channel
            stub = helloworld_pb2_grpc.GreeterStub(hw_channel)
            # await: It will just release the CPU, means suspend
            # it till the response not received from stub.SayHello(helloworld_pb2.HelloRequest(name=name))
            # Its a single threaded only, but CPU will be used for other works during wait time
            response = await stub.SayHello(helloworld_pb2.HelloRequest(name=name))
            print("Greeter client received: " + response.message)
            return response
        except grpc.aio.AioRpcError as ex:
            raise ex


def run_greet():
    client = HelloWorldClient()
    client.make_channel()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(client.greet(name="Python"))
    # asyncio.run(client.greet())  #  Will work in py3.7
    print(f'Result: {result}')

"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/grpc_exp/async_client_server_exp2
$ python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. helloworld.proto
"""

if __name__ == '__main__':
    logging.basicConfig()
    run_greet()
