from pydantic import BaseModel


class HypervisorManagerPostRequest(BaseModel):
    ipAddress: str
    username: str
    password: str
    name: str


class HypervisorManagerPostResponse(BaseModel):
    ipAddress: str
    username: str
    password: str
    name: str
    id: str
