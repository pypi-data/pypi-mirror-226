import grpc
from cbt_map_transformer.transformer.transformer_pb2_grpc import CBTMapTransformerStub
from cbt_map_transformer.transformer.transformer_pb2 import CBTMapTransformerRequest

channel = grpc.insecure_channel("localhost:5001")
client = CBTMapTransformerStub(channel)

request = CBTMapTransformerRequest(cbt_map_file_path="/tmp/cbt_maps/uuid.map")
response = client.Transform(request)
print(f'Response: {response}')
