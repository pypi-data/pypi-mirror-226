import json
import sys

data = [
    {
        "virtualMachine": {
            "hypervisorHostInfo": {
                "id": "cc11c15b-ff33-5658-8430-cb996243eb25",
                "name": "172.17.6.102"
            },
            "appInfo": {
                "vmware": {
                    "moref": "vm-88",
                    "datastoresInfo": [
                        {
                            "id": "d1f8e991-9cb0-5004-a110-6a8a81d8d51d",
                            "name": "3PAR_VOL_DS2"
                        }
                    ],
                    "toolsInfo": {
                        "type": None,
                        "version": "0",
                        "status": "NotInstalled"
                    },
                    "datacenterInfo": {
                        "moref": "datacenter-3",
                        "name": "Datacenter1"
                    }
                }
            },
            "hypervisorManagerInfo": {
                "id": "8da4e043-76df-4d44-8e97-4925979bb64f",
                "name": "VMware vCenter Server"
            },
            "computeInfo": {
                "memory_size": "4096",
                "num_cpu_cores": 2,
                "num_cpu_threads": 4
            },
            "resourceName": "bbbbbbb-1111",
            "type": "VMFS",
            "guestInfo": {
                "name": None,
                "type": None
            },
            "stateReason": "Ok",
            "networkAddress": None,
            "resourcePoolInfo": {
                "moref": "resgroup-9"
            },
            "networksInfo": [
                {
                    "id": "f74582a0-ee62-5339-b832-8b6bd725f1c1",
                    "name": "VM Network"
                }
            ],
            "createdAt": "2020-12-10T06:42:13.385Z",
            "uid": "42129e9e-5f65-42bc-80f7-ace407cf63ce",
            "powerState": "Off",
            "appType": "VMware",
            "clone": False,
            "name": "bbbbbbb-1111",
            "id": "8fede624-0168-500a-9e2c-66badfa90923",
            "state": "Ok",
            "vmConfigPath": "[3PAR_VOL_DS2] bbbbbbb/bbbbbbb.vmx",
            "status": "Ok",
            "updatedAt": "2020-12-10T06:42:13.385Z",
            "virtualDisks": [
                {
                    "uid": "6000C291-d348-a19b-a68a-b0f56d2fa7f0",
                    "capacityInBytes": 1073741824,
                    "appInfo": {
                        "vmware": {
                            "diskUuidEnabled": "true",
                            "datastoreInfo": {
                                "name": "3PAR_VOL_DS2",
                                "id": "d1f8e991-9cb0-5004-a110-6a8a81d8d51d"
                            },
                            "type": "VMFS"
                        }
                    },
                    "filePath": "[3PAR_VOL_DS2] bbbbbbb/bbbbbbb.vmdk",
                    "name": "Hard disk 1",
                    "id": "ad62cdda-9fba-56df-bb4f-353a785e9881"
                },
                {
                    "uid": "6000C291-55c1-0922-58a2-0bfe4eb73293",
                    "capacityInBytes": 1073741824,
                    "appInfo": {
                        "vmware": {
                            "diskUuidEnabled": "null",
                            "datastoreInfo": {
                                "name": "3PAR_VOL_DS2",
                                "id": "d1f8e991-9cb0-5004-a110-6a8a81d8d51d"
                            },
                            "type": "VMFS"
                        }
                    },
                    "filePath": "[3PAR_VOL_DS2] bbbbbbb/bbbbbbb_1.vmdk",
                    "name": "Hard disk 2",
                    "id": "6832a986-a587-5e87-bb9d-9aea4dc0d5a6"
                }
            ]
        }
    }

] *10000
print(data)
print(f'Memory Size of data: {sys.getsizeof(data)}')  # 44
json_str = json.dumps(data)
print(json_str)
print(type(json_str))
print(f'Length of json string: {len(json_str)}')  # 174 char
print(f'Memory Size of json string: {sys.getsizeof(json_str)}')  # 199
print(f'Size of json string: {len(json_str.encode("utf-8"))}')  # 174 bytes

MAX_JSON_SIZE = 128 * 1024 * 1024 #(134217728)bytes

if len(json_str) > MAX_JSON_SIZE:
    print(f'Sending in batches')
else:
   print(f'Sending in one chunk')