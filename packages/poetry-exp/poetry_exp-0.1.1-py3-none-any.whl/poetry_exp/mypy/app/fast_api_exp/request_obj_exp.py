from fastapi import FastAPI
from starlette.requests import Request
from pydantic import BaseModel


class User(BaseModel):
    name: str
    gender: str


app = FastAPI()


@app.post("/users")
def create_user(request_obj: Request, user: User):
    print(f'Request obj: {request_obj.__dict__}')
    print(f'User: {user}')
    user_dict = user.dict()
    user_dict['id'] = 1
    return user_dict


"""
POST: http://127.0.0.1:8000/users

Headers:
Content-Type: application/json
X-Auth-Token: 2433-3243nkdnf12-dsfsdmfnd

Request obj:
{
  'scope': {
    'type': 'http',
    'asgi': {
      'version': '3.0',
      'spec_version': '2.1'
    },
    'http_version': '1.1',
    'server': ('127.0.0.1',
    8000),
    'client': ('127.0.0.1',
    60853),
    'scheme': 'http',
    'method': 'POST',
    'root_path': '',
    'path': '/users',
    'raw_path': b'/users',
    'query_string': b'',
    'headers': [
      (b'host',
      b'127.0.0.1:8000'),
      (b'connection',
      b'keep-alive'),
      (b'content-length',
      b'44'),
      (b'x-auth-token',
      b'2433-3243nkdnf12-dsfsdmfnd'),
      (b'sec-ch-ua-mobile',
      b'?0'),
      (b'user-agent',
      b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'),
      (b'sec-ch-ua',
      b'"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"'),
      (b'sec-ch-ua-platform',
      b'"Windows"'),
      (b'content-type',
      b'application/json'),
      (b'accept',
      b'*/*'),
      (b'sec-fetch-site',
      b'none'),
      (b'sec-fetch-mode',
      b'cors'),
      (b'sec-fetch-dest',
      b'empty'),
      (b'accept-encoding',
      b'gzip, deflate, br'),
      (b'accept-language',
      b'en-US,en;q=0.9,hi;q=0.8')
    ],
    'app': <fastapi.applications.FastAPIobjectat0x05E9EFF0>,
    'router': <fastapi.routing.APIRouterobjectat0x05EB4030>,
    'endpoint': <functioncreate_userat0x063BAC48>,
    'path_params': {
      
    }
  },
  '_receive': <boundmethodRequestResponseCycle.receiveof<uvicorn.protocols.http.h11_impl.RequestResponseCycleobjectat0x063D2390>>,
  '_send': <functionExceptionMiddleware.__call__.<locals>.senderat0x063BAED0>,
  '_stream_consumed': True,
  '_is_disconnected': False,
  '_body': b'{\n  "name": "Admin",\n  "gender": "Male"\n  \n}',
  '_headers': Headers({
    'host': '127.0.0.1:8000',
    'connection': 'keep-alive',
    'content-length': '44',
    'x-auth-token': '2433-3243nkdnf12-dsfsdmfnd',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-platform': '"Windows"',
    'content-type': 'application/json',
    'accept': '*/*',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8'
  }),
  '_json': {
    'name': 'Admin',
    'gender': 'Male'
  },
  '_query_params': QueryParams(''),
  '_cookies': {
    
  }
}
"""