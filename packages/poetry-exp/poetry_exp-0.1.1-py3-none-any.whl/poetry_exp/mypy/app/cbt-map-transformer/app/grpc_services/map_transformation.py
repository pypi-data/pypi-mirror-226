# (C) Copyright 2021 Hewlett Packard Enterprise Development Company, L.P.

import grpc

from app.grpc_lib.protos.cbt_map.v1 import cbt_map_pb2_grpc
from app.grpc_lib.protos.cbt_map.v1.cbt_map_pb2 import CBTMapTransformerResponse
from app.common import constants
from app.utils import logger

LOG = logger.get_logger(__name__)


class CBTMapTransformationService(cbt_map_pb2_grpc.CBTMapTransformerServicer):
    """
    Handles map transformation
    """

    def __init__(self):
        pass

    def Transform(self, request, context):
        """
        Handles CBT Map transformation
        :param request: gRPC request
        :param context: gRPC context
        """
        LOG.info("HM Create Request params: [%s]" % request)
        req_param = request
        # payload = req_param['payload']
        # task_response = None
        try:
            print(f'Received transformation request...')
            cbt_map_file_path = request.cbt_map_file_path
            if not request.cbt_map_file_path:
                context.abort(grpc.StatusCode.NOT_FOUND, "CBT map file path not found in request")

            print(f'Transforming the CBT map: {cbt_map_file_path}')
            # Logic to transform the map and write it to file

            transformed_map_file_path = "/tmp/cbt_maps/transformations/uuid1.txt"
            print(f'Successfully transformed the CBT map: {cbt_map_file_path},'
                  f' saved the result in file: {transformed_map_file_path}')

            return CBTMapTransformerResponse(transformed_map_file_path=transformed_map_file_path)

        except Exception as ex:
            context.set_code(grpc.StatusCode.UNKNOWN)
            LOG.error("Unknown exception while registering: %s" % str(ex))
