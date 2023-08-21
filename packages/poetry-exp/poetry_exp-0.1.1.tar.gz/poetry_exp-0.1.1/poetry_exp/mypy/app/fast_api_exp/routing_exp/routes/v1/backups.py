from fastapi import APIRouter, responses, Request
from fastapi.param_functions import Header
import json
import uuid
from app.fast_api_exp.routing_exp.schemas.v1 import backups, tasks
router = APIRouter()


@router.get("", status_code=200)
async def get_backups():
    return [{"id": 1, "name": "backup1"}]


@router.post("", response_model=tasks.TaskResponse, status_code=202)
async def create_backup(request_obj: Request, request_body: backups.BackupPostRequest, authorization: str=Header(...) ):
    try:
        print(f'Creating backup with request_obj:{request_obj}, request_body:{request_body}, authorization:{authorization}')
        request_body_json_str = request_body.json(exclude_none=True)
        request_body_dict = json.loads(request_body_json_str)
        print(request_body_dict)
        request_body_dict.update({"id":1})
        return {"taskUri": "/api/v1/" + str(uuid.uuid4())}
    except Exception as e:
        return responses.JSONResponse({"error": str(e)}, status_code=500)
