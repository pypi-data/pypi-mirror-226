from django.views import View
from django.http import JsonResponse
import json
from uuid import uuid4

class Users(View):
    http_method_names = ['get', 'post']

    def __init__(self):
        pass

    def get(self, request):
        users = [
            {
                "id": 1,
                "name": "Ajay"
            },
            {
                "id": 2,
                "name": "Aman"
            }
        ]
        return JsonResponse(users, safe=False, status=200)

    def post(self, request):
        req_body = json.loads(request.body)
        user = {
            'id': str(uuid4()),
            'name': req_body['user']['name']
        }
        return JsonResponse(user, safe=False, status=200)
