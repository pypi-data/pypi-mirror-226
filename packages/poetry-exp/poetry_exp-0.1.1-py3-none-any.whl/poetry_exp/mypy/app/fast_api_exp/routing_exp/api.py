from fastapi import FastAPI, responses
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from app.fast_api_exp.routing_exp.routes import v1
from typing import Optional, List
import importlib
from app.fast_api_exp.routing_exp.routes.v1 import backups, vms
from starlette.exceptions import HTTPException
from http import HTTPStatus
import uvicorn


class ApiService(FastAPI):
    def __init__(self, conf=None):
        super().__init__(
            description=conf.description,
            title=conf.title,
            version=conf.version,
            on_startup=[self.startup_event],
            on_shutdown=[self.shutdown_event]
        )
        self.configuration = conf
        for middleware in conf.middleware:
            package_path, class_name = middleware.rsplit(".", 1)
            package = importlib.import_module(package_path)
            self.add_middleware(getattr(package, class_name))

    def initialize(self):
        print(f'Initializing...')
        v1.initialize_routes(self)
        self.add_exception_handler(HTTPException, self.http_exception_handler)
        self.add_exception_handler(RequestValidationError, self.request_validation_error_handler)

    async def startup_event(self):
        print("Starting the API service...")

    async def shutdown_event(self):
        print("Shutting down the API service...")

    async def http_exception_handler(self, request, ex: HTTPException):
        print(f'Http exception occurred: {ex}')
        error_dict = {
            "error": "Internal server error",
            "errorCode": 500
        }
        if ex.status_code == HTTPStatus.NOT_FOUND:
            error_dict = {
                "error": "URL does not exists",
                "errorCode": 404
            }
            return responses.JSONResponse(content=error_dict, status_code=ex.status_code)
        elif ex.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            error_dict = {
                "error": "Method not implemented",
                "errorCode": 404
            }
            return responses.JSONResponse(content=error_dict, status_code=ex.status_code)
        else:
            return responses.JSONResponse(content=error_dict, status_code=500)

    async def request_validation_error_handler(self, request, ex: RequestValidationError):
        print(f'Request validation failed, error: {str(ex)}')
        errors = []
        for errs in ex.errors():
            exception_loc = "-> ".join(
                [str(loc) for loc in errs["loc"]
                 if str(loc) != "__root__"])
            err_message = str(errs["msg"] + " in " + exception_loc)
            errors.append(err_message)

        error_dict = {
            "error": str(errors),
            "errorCode": 400
        }
        return responses.JSONResponse(
            content=error_dict,
            status_code=HTTPStatus.BAD_REQUEST
        )


class ConfSettings(BaseModel):
    version: str = "1.0"
    title: str = "Fast API app"
    description: str = "Fast API App"
    middleware: Optional[List[str]] = [
        "app.fast_api_exp.routing_exp.middlewares.auth.AuthMiddleware"
    ]


conf = ConfSettings()
app = ApiService(conf)
app.initialize()

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=9003)   # http://localhost:9003/docs

# OR
# ver = "/api/v1"
# app.include_router(backups.router, prefix=ver + "/" + "backups", tags=["backups"])
# app.include_router(vms.router, prefix=ver + "/" + "vms", tags=["virtual-machines"])

"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/fast_api_exp/routing_exp
$ uvicorn.exe api:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\fast_api_exp\\routing_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [10912] using statreload
INFO:     Started server process [6488]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


Browse: http://127.0.0.1:8000/api/v1/backups
[{"id":1,"name":"backup1"}]

Initializing...
Authenticating and authorizing the api endpoint:/api/v1/vms
Starting the API service...
INFO:     127.0.0.1:59372 - "GET /api/v1/backups HTTP/1.1" 200 OK


"""