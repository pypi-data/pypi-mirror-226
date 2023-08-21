# from virtual_machines import VmHardwareCustomization, \
#     RestoreVirtualMachinePayload

from pydantic import (
    BaseModel,
    constr,
    Extra,
    root_validator
)
from enum import Enum
from typing import Optional, List


class NetworkDetails(BaseModel):
    id: constr(min_length=36, max_length=36, strict=True)
    connectAtPowerOn: Optional[bool]

    class Config:
        extra = Extra.forbid


class NetworkAdaptors(BaseModel):
    name: Optional[constr(min_length=1, max_length=255, strict=True)]
    networkDetails: Optional[NetworkDetails]

    class Config:
        extra = Extra.forbid


class VmHardwareCustomization(BaseModel):
    networkAdapters: List[NetworkAdaptors]

    class Config:
        extra = Extra.forbid


class StorageInfo(BaseModel):
    storageSystemId: constr(strict=True)

    class Config:
        extra = Extra.forbid


class Vmware(BaseModel):
    datastoreId: constr(max_length=36, min_length=36, strict=True)
    resourcePoolId: Optional[constr(max_length=36, min_length=36, strict=True)]

    class Config:
        extra = Extra.forbid


class AppInfo(BaseModel):
    vmware: Vmware

    class Config:
        extra = Extra.forbid


class TargetVMInfo(BaseModel):
    name: Optional[constr(min_length=1, max_length=255, strict=True)]
    description: Optional[constr(min_length=1, max_length=255, strict=True)]
    hypervisorManagerId: Optional[constr(max_length=36,
                                         min_length=36, strict=True)]
    powerOn: Optional[bool]
    folderId: Optional[constr(max_length=36, min_length=36, strict=True)]
    hostId: Optional[constr(max_length=36, min_length=36, strict=True)]
    clusterId: Optional[constr(max_length=36, min_length=36, strict=True)]
    appInfo: Optional[AppInfo]
    storageInfo: Optional[StorageInfo]
    vmHardwareCustomization: Optional[VmHardwareCustomization]

    class Config:
        extra = Extra.forbid


class RestoreType(str, Enum):
    parent = 'Parent'
    alternate = 'Alternate'

    class Config:
        extra = Extra.forbid

def validate_vm_restore_type(cls, values):
    """
    Validate request body for restoring from backup or snapshot
    """
    if values:
        restore_type = values.get("restoreType")
        if restore_type and restore_type == 'Alternate':
            target_vm_info = values.get("targetVMInfo")
            if not target_vm_info:

                raise Exception(f"TargetVmInfo not found, values: {values}")
    return values


class RestoreVirtualMachinePayload(BaseModel):
    id: constr(max_length=36, min_length=36, strict=True)
    snapshotId: Optional[constr(max_length=36, min_length=36, strict=True)]
    backupId: Optional[constr(max_length=36, min_length=36, strict=True)]
    restoreType: RestoreType
    targetVMInfo: Optional[TargetVMInfo]

    class Config:
        extra = Extra.forbid

    # validators
    _validate_vm_restore_type = root_validator(
        validate_vm_restore_type, allow_reuse=True
    )




class RestoreVirtualMachineRequest(BaseModel):
    payload: RestoreVirtualMachinePayload

    class Config:
        extra = Extra.forbid

a = {'snapshotId': '1b2aba42-e4ef-4f33-ac5d-781629551ccc',
 'restoreType': 'Alternate',
 'targetVMInfo': {'name': 'test23435',
 'powerOn': True, 'hostId': 'cc11c15b-ff33-5658-8430-cb996243eb25',
 'appInfo': {'vmware': {'datastoreId': '354c7a13-5394-59dc-8e0d-768494e6d44a'}},
 'vmHardwareCustomization': {'networkAdapters': [{'name': 'Network adapter 1', 'networkDetails': {'id': 'f74582a0-ee62-5339-b832-8b6bd725f1c1', 'connectAtPowerOn': False}}]}}, 'id': '0a8427a3-10c3-5810-93e7-2d7e8344a557'}

x = RestoreVirtualMachinePayload(**a)
print(x, x.json())



"""

id='0a8427a3-10c3-5810-93e7-2d7e8344a557' snapshotId='1b2aba42-e4ef-4f33-ac5d-781629551ccc'
 backupId=None restoreType=<RestoreType.alternate: 'Alternate'> targetVMInfo=TargetVMInfo(name='test23435',
  description=None, hypervisorManagerId=None, powerOn=True, folderId=None,
   hostId='cc11c15b-ff33-5658-8430-cb996243eb25', clusterId=None,
    appInfo=AppInfo(vmware=Vmware(datastoreId='354c7a13-5394-59dc-8e0d-768494e6d44a', resourcePoolId=None)),
     storageInfo=None, vmHardwareCustomization=VmHardwareCustomization(networkAdapters=[NetworkAdaptors(
     name='Network adapter 1', networkDetails=NetworkDetails(id='f74582a0-ee62-5339-b832-8b6bd725f1c1',
      connectAtPowerOn=False))]))
       
       
       {"id": "0a8427a3-10c3-5810-93e7-2d7e8344a557", "snapshotId": "1b2aba42-e4ef-4f33-ac5d-781629551ccc",
        "backupId": null, "restoreType": "Alternate", "targetVMInfo": {"name": "test23435", "description": null,
         "hypervisorManagerId": null, "powerOn": true, "folderId": null, "hostId":
          "cc11c15b-ff33-5658-8430-cb996243eb25", "clusterId": null, "appInfo": {"vmware": {"datastoreId":
           "354c7a13-5394-59dc-8e0d-768494e6d44a", "resourcePoolId": null}}, "storageInfo": null,
            "vmHardwareCustomization": {"networkAdapters": [{"name": "Network adapter 1", "networkDetails":
             {"id": "f74582a0-ee62-5339-b832-8b6bd725f1c1", "connectAtPowerOn": false}}]}}}



FOr following input: change targteVMInof1

a = {'snapshotId': '1b2aba42-e4ef-4f33-ac5d-781629551ccc',
 'restoreType': 'Alternate',
 'targetVMInfo': {'name': 'test23435',
 'powerOn': True, 'hostId': 'cc11c15b-ff33-5658-8430-cb996243eb25',
 'appInfo1': {'vmware': {'datastoreId': '354c7a13-5394-59dc-8e0d-768494e6d44a'}},
 'vmHardwareCustomization': {'networkAdapters': [{'name': 'Network adapter 1', 'networkDetails': {'id': 'f74582a0-ee62-5339-b832-8b6bd725f1c1', 'connectAtPowerOn': False}}]}}, 'id': '0a8427a3-10c3-5810-93e7-2d7e8344a557'}

C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/pydantic_example/validate_vm_request.py"
Traceback (most recent call last):
  File "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/pydantic_example/validate_vm_request.py", line 130, in <module>
    x = RestoreVirtualMachinePayload(**a)
  File "C:\Python3\lib\site-packages\pydantic\main.py", line 404, in __init__
    values, fields_set, validation_error = validate_model(__pydantic_self__.__class__, data)
  File "C:\Python3\lib\site-packages\pydantic\main.py", line 1066, in validate_model
    values = validator(cls_, values)
  File "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/pydantic_example/validate_vm_request.py", line 93, in validate_vm_restore_type
    raise Exception(f"TargetVmInfo not found, values: {values}")
Exception: TargetVmInfo not found, values: {'id': '0a8427a3-10c3-5810-93e7-2d7e8344a557', 'snapshotId': '1b2aba42-e4ef-4f33-ac5d-781629551ccc', 'backupId': None, 'restoreType': <RestoreType.alternate: 'Alternate'>}

Process finished with exit code 1

"""