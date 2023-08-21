import grpc
from app.grpc_lib.protos.cbt_map.v1.cbt_map_pb2_grpc import CBTMapTransformerStub
from app.grpc_lib.protos.cbt_map.v1.cbt_map_pb2 import CBTMapTransformerRequest

from app.common import constants


channel = grpc.insecure_channel("localhost:50051")
client = CBTMapTransformerStub(channel)
print(f'...client: {client}')
request = CBTMapTransformerRequest(cbt_map_file_path="/tmp/cbt_maps/uuid.map")
response = client.Transform(request)
print(f'Response: {response}')
