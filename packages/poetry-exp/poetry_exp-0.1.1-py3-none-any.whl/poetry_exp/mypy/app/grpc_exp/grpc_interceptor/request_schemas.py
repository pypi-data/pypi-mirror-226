from pydantic import BaseModel, constr, conint, root_validator
from typing import Optional


class InvalidArgument(Exception):
    pass


def validate_retention_unit(cls, values):
    if values and values.get("retentionUnit") is not None:
        retention_unit = values.get("retentionUnit")
        if retention_unit not in ['Days', 'Months', 'Years']:
            err_msg = 'Invalid retention unit provided'
            print(err_msg)
            raise InvalidArgument(err_msg)
    return values


class CreateBackupPayload(BaseModel):
    name: constr(min_length=1, max_length=255, strict=True)
    description: Optional[constr(min_length=1, max_length=255, strict=True)]
    retention: conint(ge=1)
    retentionUnit: str
    resourceId: constr(min_length=36, max_length=36, strict=True)
    # validators
    _validate_expire_after_unit = root_validator(
        validate_retention_unit, allow_reuse=True
    )