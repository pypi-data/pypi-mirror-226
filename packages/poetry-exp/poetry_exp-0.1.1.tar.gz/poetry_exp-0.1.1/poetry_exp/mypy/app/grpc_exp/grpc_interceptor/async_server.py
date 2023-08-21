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
from request_schemas import CreateBackupPayload, InvalidArgument
from interceptor import GrpcInterceptor

import backup_pb2
import backup_pb2_grpc


def schema_validator(model):
    def wrapper(function):
        def decorated_func(self, request, context):
            try:
                # When client will call
                # This request comes here as protobuf request(backuppb2.BackupRequest)
                request = model(**MessageToDict(request))
                request = request.json(exclude_none=True)
                # now the request we are sending as dict
                return function(
                    self, json.loads(request), context)
            except ValidationError as ex:
                print("Failed to aafak111 validate schema %s" % str(ex))
                errors = []
                for errs in ex.errors():
                    exception_loc = "->".join(
                        [str(loc) for loc in errs["loc"]
                         if str(loc) != "__root__"])
                    err_message = str(errs["msg"] + " in " + exception_loc)
                    errors.append(err_message)
                error_dict = {"errors": errors}
                # context.abort(grpc.StatusCode.INVALID_ARGUMENT, json.dumps(error_dict))
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(json.dumps(error_dict))
            except InvalidArgument as ex:
                print("Schema aafak222 validation failed: %s" % str(ex))
                #context.abort(grpc.StatusCode.INTERNAL, str(ex))
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(str(ex))
        return decorated_func

    print(f'Test4, wrapper: {wrapper}')

    return wrapper


class BackupService(backup_pb2_grpc.BackupServicer):

    @schema_validator(model=CreateBackupPayload)
    def Create(
            self, request, context):
        response = None
        try:
            logging.info(f"Received backup request, request: {request}, processing..., context: {dir(context)}")
            # if request["retentionUnit"] not in ['Days', 'Months', 'Years']:
            #     #context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Failed to create Backup invalid id")
            #     context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            #     context.set_details('Failed to create Backup invalid retention unit')
            #     return response
            taskId = str(uuid.uuid4())
            logging.info(f"Backup request submitted successfully taskID: {taskId}")
            response = backup_pb2.BackupResponse(taskId=taskId)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to create Backup')
            print(e)

        return response


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #asyncio.run(serve())  # will work in python3.7
    #asyncio.run(serve())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve())
