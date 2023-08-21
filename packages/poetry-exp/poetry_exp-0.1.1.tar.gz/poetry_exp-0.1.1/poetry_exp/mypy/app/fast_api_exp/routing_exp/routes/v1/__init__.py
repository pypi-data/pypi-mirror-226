from fastapi import FastAPI
from app.fast_api_exp.routing_exp.routes.v1 import backups, vms


def initialize_routes(cls: FastAPI, ver=None):

    if ver is None:
        ver = "/api/v1"

    cls.include_router(backups.router, prefix=ver + "/" + "backups", tags=["backups"])
    cls.include_router(vms.router, prefix=ver + "/" + "vms", tags=["virtual-machines"])