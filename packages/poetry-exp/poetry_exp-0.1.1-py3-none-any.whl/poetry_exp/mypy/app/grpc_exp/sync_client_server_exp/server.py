"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print(f'Request received...{request}')
        if request.gender == helloworld_pb2.Gender.GENDER_MALE:
            print(f'Request received from Male: {request.gender}')
            response = helloworld_pb2.HelloReply(
                name='Hell1, %s!' % request.name,
                status=helloworld_pb2.Status.STATUS_SUCCESS,
                gender=helloworld_pb2.Gender.GENDER_MALE, age=request.age)
        elif request.gender == helloworld_pb2.Gender.GENDER_FEMALE:
            print(f'Request received from Female: {request.gender}')
            response = helloworld_pb2.HelloReply(
                name='Hell1, %s#' % request.name,
                status=helloworld_pb2.Status.STATUS_SUCCESS,
                gender=helloworld_pb2.Gender.GENDER_FEMALE, age=request.age)
            # response = helloworld_pb2.HelloReply()
        else:
            print(f'Request received from invalid gender: {request.gender}')
            response = helloworld_pb2.HelloReply(
                name='Hell1, %s#' % request.name,
                status=helloworld_pb2.Status.STATUS_ERROR,
                gender=request.gender, age=request.age)

        print(f'Returning response: {response}')
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Starting the server...')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()


"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/grpc_exp/sync_client_server_exp
$ python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. helloworld.proto

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/grpc_exp/sync_client_server_exp
$


"""