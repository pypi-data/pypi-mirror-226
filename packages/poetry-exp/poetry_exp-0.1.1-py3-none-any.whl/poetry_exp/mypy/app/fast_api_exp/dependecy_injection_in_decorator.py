"""
In some cases you don't really need the return value of a dependency inside your path operation function.

Or the dependency doesn't return a value.

But you still need it to be executed/solved.

For those cases, instead of declaring a path operation function parameter with Depends,
you can add a list of dependencies to the path operation decorator.
"""

from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Request
from fastapi.param_functions import Header
import uvicorn


def verify_token(authorization: str = Header(...)):
    print(f'Verifying token...authorization: {authorization}')
    if authorization is None:
        """
        will raise automatically following exception if authorization field not supplied in header
        {
                "detail": [
                    {
                        "loc": [
                            "header",
                            "authorization"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }

        """
        print('Error: Authorization field not supplied in headers')
    if authorization != 'test':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


router = APIRouter()


def log_request_parm(request: Request):
    print(f'Request: {request}')
    print(f'Request Headers: {request.headers}')


def get_request_header(request: Request):
    print(f'Getting header from Request: {request}')
    print(f'Request Headers: {request.headers}')
    return request.headers


def get_token(request: Request):
    print(f'Getting token from Request Headers: {request.headers}, type: {type(request.headers)}')
    return request.headers['authorization']

# First log_request_parm will execute and then verify_token will execute
@router.get("/products", dependencies=[Depends(log_request_parm), Depends(verify_token)])
def get_products(request: Request):
    print(f'request headers: {request.headers}')
    return [{"id": 1, "name": "p1", "price": 100}]


# First verify_token will execute and then get_request_header will execute
@router.get("/users", dependencies=[Depends(verify_token)])
def get_products(request_obj: Request, header: Header = Depends(get_request_header)):
    print(f'request_obj: {request_obj}')
    print(f'request headers: {header}')
    return [{"id": 1, "name": "u1"}]


# First get_token will execute aand then get_request_header will execute
@router.get("/items")
def get_products(token: str = Depends(get_token),
                 header: Header = Depends(get_request_header)):
    print(f'Token: {token}')
    print(f'Header: {header}')
    return [{"id": 1, "name": "item1"}]


if __name__ == '__main__':
    app = FastAPI()
    # add dependencies to the whole application
    # app = FastAPI(dependencies=[Depends(verify_token)])

    app.include_router(router, prefix="/api/v1", tags=["dependency injection"])

    uvicorn.run(app, host='localhost', port=8000, log_level="info")


"""
GET:
 http://127.0.0.1:8000/api/v1/products
Headers:
   Authorization: test

authorization: test
request headers: Headers({'host': '127.0.0.1:8000', 'connection': 'keep-alive', 'authorization': 'test', 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"', 'sec-ch-ua-platform': '"Windows"', 'accept': '*/*', 'sec-fetch-site': 'none', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9,hi;q=0.8'})
INFO:     127.0.0.1:63538 - "GET /api/v1/products HTTP/1.1" 200 OK
"""