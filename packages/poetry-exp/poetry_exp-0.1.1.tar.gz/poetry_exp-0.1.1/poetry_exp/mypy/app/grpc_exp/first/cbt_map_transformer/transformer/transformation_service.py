from concurrent import futures

import grpc

from app.grpc_exp.first.cbt_map_transformer.transformer import transformer_pb2_grpc
from app.grpc_exp.first.cbt_map_transformer.transformer.transformer_pb2 import CBTMapTransformerResponse


class TransformationService(transformer_pb2_grpc.CBTMapTransformerServicer):
    def Transform(self, request, context):
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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transformer_pb2_grpc.add_CBTMapTransformerServicer_to_server(
        TransformationService(), server
    )
    server.add_insecure_port("[::]:50051")
    print('Starting the server...')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()