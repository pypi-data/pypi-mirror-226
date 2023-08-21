# (C) Copyright 2021 Hewlett Packard Enterprise Development Company, L.P.

import os
import asyncio
from grpc import aio


from app.grpc_lib.protos.cbt_map.v1 import cbt_map_pb2_grpc

from app.grpc_services.map_transformation import CBTMapTransformationService
from app.utils import logger
from app.common import constants

LOG = logger.get_logger(__name__)


def add_servicer(server):
    # CBT map transformation servicer
    cbt_map_pb2_grpc.add_CBTMapTransformerServicer_to_server(
        CBTMapTransformationService(), server)


async def start_server():
    server = aio.server()
    # TODO : secure connection
    server.add_insecure_port('[::]:' + constants.SERVER_PORT)

    # Add servicer
    add_servicer(server)

    await server.start()
    LOG.info("gRPC server listening on port %s" % constants.SERVER_PORT)
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(start_server())
