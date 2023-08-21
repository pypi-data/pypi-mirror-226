from fastapi import FastAPI
from starlette.requests import Request
from pydantic import BaseModel
from fastapi.param_functions import Header


class User(BaseModel):
    name: str
    gender: str


class UserResponse(BaseModel):
    name: str
    id: int
    gender: str


app = FastAPI()


@app.post("/users", status_code=202, response_model=UserResponse)
def create_user(request_obj: Request, user: User, authorization: str = Header(...)):
    # print(f'Request obj: {request_obj.__dict__}')
    print(f'....Authorization obj: {authorization}')

    print(f'User: {user}')
    user_dict = user.dict()
    user_dict['id'] = 1
    return user_dict


"""
POST: http://127.0.0.1:8000/users

Headers:
Content-Type: application/json
X-Auth-Token: 2433-3243nkdnf12-dsfsdmfnd
authorization: xyz

WARNING:  StatReload detected file change in 'authorization_exp.py'. Reloading...
INFO:     Started server process [107744]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
....Authorization obj: xyz
User: name='Admin' gender='Male'
INFO:     127.0.0.1:58840 - "POST /users HTTP/1.1" 202 Accepted

"""