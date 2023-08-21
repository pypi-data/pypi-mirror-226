from fastapi import APIRouter, responses

router = APIRouter()


@router.get("")
async def get_vms():
    try:
        return [{"id": 1, "name": "vm1"}]
    except Exception as e:
        error_details = {
            "error": str(e),
            "error_code": "INTERNAL_ERROR"
        }
        return responses.JSONResponse(content=error_details, status_code=500)
