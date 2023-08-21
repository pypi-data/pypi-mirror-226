# https://fastapi.tiangolo.com/tutorial/query-params/

from fastapi import FastAPI
from typing import Optional

app = FastAPI()

fake_users_db = []
for i in range(100):
    fake_users_db.append({
        'id': i,
        'name': "user" + str(i)
    })


#http://127.0.0.1:8000/users?skip=0&limit=21
@app.get("/users")
def get_users(skip: int = 0, limit: int = 10):
    return fake_users_db[skip: skip + limit]


# http://127.0.0.1:8000/users/1/items/1?short=true&q=hello
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/fast_api_exp
$ uvicorn query_exp:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\fast_api_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [81876] using statreload
INFO:     Started server process [95068]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:58945 - "GET /users?skip=0&limit=5 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61902 - "GET /users?skip=0&limit=21 HTTP/1.1" 200 OK
WARNING:  StatReload detected file change in 'query_exp.py'. Reloading...


http://127.0.0.1:8000/users?skip=0&limit=21
"""