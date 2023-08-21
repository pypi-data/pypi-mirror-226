"""The Python AsyncIO implementation of the GRPC helloworld.Greeter client."""

import logging
import asyncio
import grpc

import backup_pb2
import backup_pb2_grpc
from request_schemas import CreateBackupPayload

from client_handler import ClientHandler

global hw_channel

SERVER = 'localhost'
PORT = '50051'


class BackupClient(ClientHandler):
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

    async def create(self, **kwargs):
        try:
            request_body = kwargs.get('request_body')
            # Validate given request body with model
            req_schema = CreateBackupPayload(**request_body)
            print(f'req_schema: {req_schema}')
            global hw_channel
            stub = backup_pb2_grpc.BackupStub(hw_channel)
            # await: It will just release the CPU, means suspend
            # it till the response not received from stub.SayHello(helloworld_pb2.HelloRequest(name=name))
            # Its a single threaded only, but CPU will be used for other works during wait time
            #request_body['resourceId'] = "a"  # To check server side error
            #request_body['retentionUnit'] = "Days1"  # To check server side error

            backup_request = backup_pb2.BackupRequest(**request_body)
            response = await stub.Create(backup_request)
            print(f"Backup create response received: {str(response)}, type: {type(response)}")
            return response
        except grpc.aio.AioRpcError as ex:
            print(f"Error: Backup RPC failed, status: {ex.code()}")
            print(ex)


def test_backup_client():
    client = BackupClient()
    client.make_channel()
    loop = asyncio.get_event_loop()
    request_body = {
        "name": "Backup1",
        "retention": 2,
        "retentionUnit": "Days",
        "resourceId": "a998815d-5205-463e-9394-0d901f7b3b3e"
    }
    result = loop.run_until_complete(client.create(request_body=request_body))
    # asyncio.run(client.greet())  #  Will work in py3.7
    print(f'Result: {result}')

if __name__ == '__main__':
    logging.basicConfig()
    test_backup_client()
