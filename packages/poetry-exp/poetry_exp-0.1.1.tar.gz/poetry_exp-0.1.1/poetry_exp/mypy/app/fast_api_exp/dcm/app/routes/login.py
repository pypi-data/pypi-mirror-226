from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.login import UserLoginRequest, UserLoginResponse
from app.db.utils import DBHelper
from app.auth.password_utils import verify_password
from app.auth import token_utils

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
def login(request_body: OAuth2PasswordRequestForm = Depends()):
    print(f'request received: {request_body}')
    db = DBHelper()
    username = request_body.username
    user = db.get_by_username("users", username)
    if user:
        password = request_body.password
        if verify_password(password, user['password']):
            return {"access_token": token_utils.create_token(username), "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")



# @router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
# def login(request_body: UserLoginRequest):
#     print(f'request received: {request_body}')
#     db = DBHelper()
#     username = request_body.username
#     user = db.get_by_username("users", username)
#     if user:
#         password = request_body.password
#         if verify_password(password, user['password']):
#             return {"token": token_utils.create_token(username)}
#         else:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")