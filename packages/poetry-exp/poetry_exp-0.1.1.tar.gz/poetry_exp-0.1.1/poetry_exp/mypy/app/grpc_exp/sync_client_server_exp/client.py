"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
from google.protobuf.json_format import MessageToDict



def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(
            name='John', gender=helloworld_pb2.Gender.GENDER_FEMALE, age='5'))
    print(f"Response: {response}")
    print(f"Status: {response.status}")
    print(f"Gender: {response.gender}")

    if response.status == helloworld_pb2.Status.STATUS_SUCCESS:
        print(f"status: {helloworld_pb2.Status.STATUS_SUCCESS}")

    response_dict = MessageToDict(response)
    print(f"response_dict: {response_dict}")

if __name__ == '__main__':
    logging.basicConfig()
    run()