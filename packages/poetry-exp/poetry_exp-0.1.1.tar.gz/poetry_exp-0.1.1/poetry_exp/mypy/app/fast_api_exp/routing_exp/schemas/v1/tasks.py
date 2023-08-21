from pydantic import BaseModel


class TaskResponse(BaseModel):
    taskUri: str