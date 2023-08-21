from fastapi import APIRouter, status
from app.schemas.users import UserRegisterRequest, UserRegisterResponse
from app.db.utils import DBHelper
from app.auth.password_utils import get_password_hash

router = APIRouter()


@router.post("/register", status_code=status.HTTP_200_OK, response_model=UserRegisterResponse)
def register(request_body: UserRegisterRequest):
    print(f'request received: {request_body}')
    db = DBHelper()
    hashed_password = get_password_hash(request_body.password)
    print(f'Creating user with hashed_password: {hashed_password}...')
    db.insert_record("users", {"username": request_body.username, "password": hashed_password})
    print('Users created successfully')
    return request_body
