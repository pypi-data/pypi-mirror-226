from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json

# .local/share/umake/ide/pycharm/bin/pycharm.sh
# Create your views here.
@api_view(["GET"])
def get_policy(request):
    try:
       # height=json.loads(heightdata.body)
       # weight=str(height*10)
       print("comes here...")
       #weight = str(5)
       return JsonResponse([{"name": "P1"}, {"name": "P2"}],safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_policy(request):
    try:
       print("Creating Policy...")
       body=json.loads(request.body)
       return JsonResponse({"id": 1, "name": "P1"},safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def update_policy(request):
    try:
       # height=json.loads(heightdata.body)
       # weight=str(height*10)
       print("comes here...")
       #weight = str(5)
       return JsonResponse([{"name": "P1"}, {"name": "P2"}],safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_policy(request):
    try:
       # height=json.loads(heightdata.body)
       # weight=str(height*10)
       print("comes here...")
       #weight = str(5)
       return JsonResponse([{"name": "P1"}, {"name": "P2"}],safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)