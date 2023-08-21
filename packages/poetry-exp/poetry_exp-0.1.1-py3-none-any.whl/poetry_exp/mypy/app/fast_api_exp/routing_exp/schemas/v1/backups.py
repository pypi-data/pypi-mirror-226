from pydantic import BaseModel, constr
from typing import Optional


class BackupPostRequest(BaseModel):
    name: constr(min_length=1, max_length=255)
    description: Optional[str]
    resourceId: constr(min_length=36, max_length=36)