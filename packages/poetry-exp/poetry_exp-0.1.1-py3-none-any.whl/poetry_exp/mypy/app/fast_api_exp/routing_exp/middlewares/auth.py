from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response, responses


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            api = request.scope["path"]
            print(f'request.headers: {request.headers}')
            auth_token = request.headers.get("authorization")
            print(f'Authenticating and authorizing the api endpoint:{api} with auth_token:{auth_token}')
            response = await call_next(request)
            return response
        except Exception as ex:
            return responses.JSONResponse(
                {
                    "error": "Error during authentication check: " + str(ex),
                    "error_code": 102,
                },
                status_code=500,
            )


