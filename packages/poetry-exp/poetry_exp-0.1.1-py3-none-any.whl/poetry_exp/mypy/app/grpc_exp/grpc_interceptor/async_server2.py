"""The Python AsyncIO implementation of the GRPC helloworld.Greeter server."""
"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/grpc_exp/grpc_interceptor
$ python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. backup.proto

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/grpc_exp/grpc_interceptor
$ ls
__init__.py  async_client.py  async_server.py  backup.proto  backup_pb2.py  backup_pb2_grpc.py  client_handler.py

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/grpc_exp/grpc_interceptor

"""


import logging
import asyncio
import grpc
import time
import json
import uuid
from pydantic import ValidationError
from google.protobuf.json_format import MessageToDict
from request_schemas import CreateBackupPayload
from interceptor import GrpcInterceptor

import backup_pb2
import backup_pb2_grpc


def schema_validator(model):
    def wrapper(function):
        def decorated_func(self, request, context):
            try:
                print(f'Test1')

                request1 = model(**MessageToDict(request))
                print(f'Test2, request1: {request}')

                # request = request.json(exclude_none=True)
                # print(f'Test3, request: {request}')
                #
                # return function(
                #     self, json.loads(request), context)
                return function(
                    self, json.loads(request), context)

            except ValidationError as ex:
                print("Failed to aafak111 validate schema %s" % str(ex))
                # errors = []
                # for errs in ex.errors():
                #     exception_loc = "->".join(
                #         [str(loc) for loc in errs["loc"]
                #          if str(loc) != "__root__"])
                #     err_message = str(errs["msg"] + " in " + exception_loc)
                #     errors.append(err_message)
                error_dict = {"error": str(ex)}
                #context.abort(grpc.StatusCode.INVALID_ARGUMENT, error_dict)
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, json.dumps(error_dict))

            except Exception as ex:
                print("Schema aafak222 validation failed: %s" % str(ex))
                context.abort(grpc.StatusCode.INTERNAL, str(ex))
                raise ex
        return decorated_func

    print(f'Test4, wrapper: {wrapper}')

    return wrapper


def schema_validator2(func):
    def validate(*args, **kwargs):
        print('Executing.....')
        return func(*args, **kwargs)
    return validate


def schema_validator3(func):
    def validate(*args, **kwargs):
        print('Executing.....')
        return func(*args, **kwargs)
    return validate

class BackupService(backup_pb2_grpc.BackupServicer):

    #@schema_validator(model=CreateBackupPayload)
    #@schema_validator2
    def Create(
            self, request, context):
        try:
            print(f'Test0')
            logging.info(f"Received backup request, request: {request}, processing..., context: {dir(context)}")

            time.sleep1(1)
            if request.resourceId == 'invalidId':
                #context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Failed to create Backup invalid id")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Failed to create Backup invalid id')
                return
            taskId = str(uuid.uuid4())
            logging.info(f"Backup request submitted successfully taskID: {taskId}")
            return backup_pb2.BackupResponse(taskId=taskId)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to create Backup')


async def serve() -> None:
    grpc_interceptor = GrpcInterceptor()
    server = grpc.aio.server(interceptors=(grpc_interceptor,))
    backup_pb2_grpc.add_BackupServicer_to_server(BackupService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


async def start_server():
    # Add interceptors to intercept grpc calls
    interceptors = (GrpcInterceptor(),)
    server = grpc.aio.server(interceptors=interceptors)
    server.add_insecure_port('[::]:50051')

    # Add servicer
    backup_pb2_grpc.add_BackupServicer_to_server(BackupService(), server)


    await server.start()
    print("gRPC server listening on port 50051")

    # def handle_sigterm(*_):
    #     LOG.info("Received shutdown signal")
    #     server.stop(30)
    #     LOG.info("Shut down gracefully")
    #
    # signal(SIGTERM, handle_sigterm)
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(start_server())
