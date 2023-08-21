from fastapi import FastAPI, APIRouter
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

router = APIRouter()
app = FastAPI()

# By enabling this , you can't do http request(http://127.0.0.1:8000/api/v1/users),
# app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1"])  # will work for localhost

# By enabling this you will get Invalid host header from localhost or any machine other than 10.10.1.1
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["10.10.1.1"])


@router.get("/users")
async def get_users():
    return [{"id": 1, "name": "user1"}]


if __name__ == '__main__':
    app.include_router(router, prefix="/api/v1", tags=['Testing Http Middleware'])
    uvicorn.run(app)


"""
Hit the http://127.0.0.1:8000/
it will redirect automatically to https://127.0.0.1:8000/
"""