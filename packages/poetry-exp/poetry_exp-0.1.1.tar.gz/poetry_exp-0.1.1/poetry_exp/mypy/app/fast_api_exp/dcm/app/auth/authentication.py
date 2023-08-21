from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from app.db.utils import DBHelper
from app.auth import token_utils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def authenticate_user(token: str = Depends(oauth2_scheme)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = token_utils.decode_token(token, cred_exc)
    username = payload.get('sub')
    db = DBHelper()
    user = db.get_by_username("users", username)
    if user:
        return user
    else:
        raise cred_exc

