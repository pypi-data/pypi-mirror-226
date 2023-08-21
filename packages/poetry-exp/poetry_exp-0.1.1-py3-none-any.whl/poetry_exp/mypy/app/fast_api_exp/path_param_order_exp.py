# https://realpython.com/fastapi-python-web-apis/#what-is-fastapi
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def get_user():
    return {
        'id': 1,
        'name': "The current user"
    }


@app.get("/users/{user_id}")
async def get_user(user_id):
    return {
        'id': user_id,
        'name': "Admin"
    }


"""
When creating path operations, you may find situations where you have a fixed path,
like /users/me. Let’s say that it’s to get data about the current user.
You might also have the path /users/{user_id} to get data about a specific user by some user ID.

Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/fast_api_exp
$ uvicorn.exe path_param_order_exp:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\fast_api_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [91716] using statreload
INFO:     Started server process [20964]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


http://127.0.0.1:8000/users/me

Response:
{"id":"1","name":"the current user"}



http://127.0.0.1:8000/users/1
{"id":1,"name":"Admin"}


Verify the docs:
http://127.0.0.1:8000/docs
"""