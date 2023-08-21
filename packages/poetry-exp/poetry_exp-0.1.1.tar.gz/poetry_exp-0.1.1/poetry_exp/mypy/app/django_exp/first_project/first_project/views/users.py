from django.views import View
from django.http import HttpResponse, JsonResponse
import json
from uuid import uuid4


class Users(View):
    http_method_names = ['get', 'post']

    def __init__(self):
        pass

    def get(self, request):
        users = [
            {
                'id': 1,
                'name': 'Ajay'
            },
            {
                'id': 2,
                'name': 'Aman'
            }
        ]
        return JsonResponse(users, safe=False, status=200)

    def post(self, request):
        request_body = json.loads(request.body)
        name = request_body['user']['name']
        id = uuid4()
        user = {
            'id': str(id),
            'name': name
        }
        # return HttpResponse(json.dumps(user), 200)
        return JsonResponse(user, safe=False, status=200)

