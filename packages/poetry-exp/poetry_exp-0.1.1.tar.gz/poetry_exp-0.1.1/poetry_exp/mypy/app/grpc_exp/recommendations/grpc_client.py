import grpc
from grpc_exp.recommendations.recommendations_pb2_grpc import RecommendationsStub
from grpc_exp.recommendations.recommendations_pb2 import RecommendationRequest
from grpc_exp.recommendations.recommendations_pb2 import BookCategory

channel = grpc.insecure_channel("localhost:50051")
client = RecommendationsStub(channel)

request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)
response = client.Recommend(request)
print(f'Response: {response}')