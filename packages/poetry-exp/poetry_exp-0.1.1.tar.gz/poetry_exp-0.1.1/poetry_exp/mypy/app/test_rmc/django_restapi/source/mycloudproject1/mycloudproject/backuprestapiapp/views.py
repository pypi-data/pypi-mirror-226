from django.shortcuts import render

# Create your views here.

# Create your views here.
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
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
