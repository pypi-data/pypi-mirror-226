from pydantic import BaseModel
from typing import Optional


class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserRegisterResponse(BaseModel):
    username: str


class User(BaseModel):
    username: str