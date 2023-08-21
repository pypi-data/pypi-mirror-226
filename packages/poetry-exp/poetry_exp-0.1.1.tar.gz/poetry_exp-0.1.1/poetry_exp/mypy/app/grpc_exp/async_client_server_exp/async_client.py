"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""

import logging
import asyncio
import grpc

import helloworld_pb2
import helloworld_pb2_grpc


async def run2() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


async def run() -> None:
    channel = grpc.aio.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = await stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    #asyncio.run(run()) # Will work in py3.7
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())