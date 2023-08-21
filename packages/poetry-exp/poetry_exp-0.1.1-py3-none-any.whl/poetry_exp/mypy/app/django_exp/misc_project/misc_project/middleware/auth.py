from django.http import JsonResponse


class Authenticate:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        error = None
        auth_token = request.headers.get('Auth-Token')
        if auth_token:
            if auth_token != 't1':
                error = {
                    "error": "Authentication Failed."
                }
        else:
            error = {
                "error": "Authentication Token Required."
            }

        if error:
            return JsonResponse(error, safe=False, status=401)

        response = self.get_response(request)
        return response
