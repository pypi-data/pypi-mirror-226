from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt


# $ pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 python-jose
"""
https://pypi.org/project/python-jose/
The JavaScript Object Signing and Encryption (JOSE) technologies - JSON Web Signature (JWS),
JSON Web Encryption (JWE), JSON Web Key (JWK), and JSON Web Algorithms (JWA) -
collectively can be used to encrypt and/or sign content using a variety of algorithms.
While the full set of permutations is extremely large, and might be daunting to some,
it is expected that most applications will only use a small set of algorithms to meet their needs.

>>> from jose import jwt
>>> token = jwt.encode({'key': 'value'}, 'secret', algorithm='HS256')
u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ2YWx1ZSJ9.FG-8UppwHaFp1LgRYQQeS6EDQF7_6-bMFegNucHjmWg'

>>> jwt.decode(token, 'secret', algorithms=['HS256'])
{u'key': u'value'}
"""


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class InvalidToken(Exception):
    pass


class TokenData(BaseModel):
    email: Optional[str] = None


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception


if __name__ == '__main__':
    data = {"sub": "aafak@yahho.com"}
    token = create_access_token(data)
    print(token)  # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYWZha0B5YWhoby5jb20iLCJleHAiOjE2NTY0ODEzOTh9.0B9mqI-5lb6bKCGsrDzhl0NyX1XXIF4e8bwoAdPe-U4

    token_data = verify_token(token, InvalidToken)
    print(token_data)  # email='aafak@yahho.com'
