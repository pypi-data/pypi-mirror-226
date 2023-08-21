# https://realpython.com/fastapi-python-web-apis/#what-is-fastapi
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id):
    return {
        'id': user_id,
        'name': "Admin"
    }


@app.get("/products/{product_id}")
async def get_product(product_id: int):    # str, float, bool
    return {
        'id': product_id,
        'name': "Sony"
    }


"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/fast_api_exp
$ uvicorn.exe path_param_exp:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\fast_api_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [91716] using statreload
INFO:     Started server process [20964]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


http://127.0.0.1:8000/users/1

Response:
{"id":"2","name":"Admin"}



http://127.0.0.1:8000/products/1
{"id":1,"name":"Sony"}


http://127.0.0.1:8000/products/abc
{"detail":[{"loc":["path","product_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}


Verify the docs:
http://127.0.0.1:8000/docs
"""