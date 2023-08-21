
def get_datastores():
    vcenter_dict = {
        "hosts": [
            {
                "moref": "host-1",
                "name": "Host1",
                "datastores": [
                    {
                        "moref": "ds-1",
                        "name": "Datastore1",
                        "vms": [
                            {
                                "moref": "vm-1",
                                "name": "vm1"
                            },
                            {
                                "moref": "vm-2",
                                "name": "vm2"
                            }
                        ]
                    },
                    {
                        "moref": "ds-2",
                        "name": "Datastore2",
                        "vms": [
                            {
                                "moref": "vm-2",
                                "name": "vm3"
                            },
                            {
                                "moref": "vm-2",
                                "name": "vm2"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    datastores = [
        {
            "moref": "ds-1",
            "name": "datastore1",
            "hostInfo":{
                "id":
            }
            "vms": [
                {
                    "moref" : "vm-1",
                    "DatastoreInfo": {
                        "id": "",
                        "name":
                    }

                }
            ]
        },
        {
            "moref": "ds-2",
            "name": "datastore2",
            "vms": ["vm-2"]
        }
    ]
    return datastores


def get_vms():
    vms = [
        {
            "moref": "vm-1",
            "name": "virtual-machine1"
        },
        {
            "moref": "vm-2",
            "name": "virtual-machine"
        }
    ]
    return vms


def build_cache():
    datastores = get_datastores()
    vms = get_vms()
    cache = {
        "vcenter1": {
            "datastores": datastores,
            "vms": vms
        }
    }

def persist_cache(cache_dict):
    for vcenter_uuid, vcenter_dict in cache_dict.items():
        datastores = vcenter_dict['datastores']
        # for datastore in datastores:
