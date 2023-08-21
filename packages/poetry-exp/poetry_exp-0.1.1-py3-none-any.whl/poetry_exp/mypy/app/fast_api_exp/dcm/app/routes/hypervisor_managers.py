from fastapi import HTTPException, APIRouter, status, Depends
from app.schemas.hypervisor_managers import HypervisorManagerPostRequest, HypervisorManagerPostResponse
from app.db.utils import DBHelper
from app.auth.authentication import authenticate_user
import uuid
from app.auth.password_utils import get_password_hash

router = APIRouter()


@router.post("/hypervisor-managers", status_code=status.HTTP_202_ACCEPTED, response_model=HypervisorManagerPostResponse)
def create_hypervisor_manager(request_body: HypervisorManagerPostRequest, current_user: dict = Depends(authenticate_user)):
    print(f'Creating hypervisor managers, request_body: {request_body}')
    db = DBHelper()
    hm_dict = {
            "id": str(uuid.uuid4()),
            "name": request_body.name,
            "ip_address": request_body.ipAddress,
            "username": request_body.username,
            "password": get_password_hash(request_body.password)
        }
    db.insert_record(
        "hypervisor_managers", hm_dict
    )
    hm_dict['ipAddress'] = request_body.ipAddress
    return hm_dict


@router.get("/hypervisor-managers", status_code=status.HTTP_200_OK)
def get_all(current_user: dict = Depends(authenticate_user)):
    print(f'Getting hypervisor_managers for user: {current_user}')
    db = DBHelper()
    result = db.get_records("hypervisor_managers")
    return result