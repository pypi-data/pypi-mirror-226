VMS = [
    # {
    #     "instanceUUID": "1",
    #     "name": "vm1",
    #     "moref": "vm-1",
    #     "datastore": "ds-1"
    # },
    {
        "instanceUUID": "2",
        "name": "vm2",
        "moref": "vm-2",
        "datastore": "ds-1"
    },
    # {
    #     "instanceUUID": "3",
    #     "name": "vm3",
    #     "moref": "vm-3",
    #     "datastore": "ds-2"
    # },
    {
        "instanceUUID": "4",
        "name": "vm4",
        "moref": "vm-4",
        "datastore": "ds-2"
    },
    {
        "instanceUUID": "5",
        "name": "vm5",
        "moref": "vm-5",
        "datastore": "ds-3"
    },
    {
        "instanceUUID": "6",
        "name": "vm6",
        "moref": "vm-6",
        "datastore": "ds-3"
    }
]


DATASTORES = [
    {
        "instanceUUID": "1",
        "name": "datastore1",
        "moref": "ds-1",
        "vms": ["vm-1", "vm-2"]
    },
    {
        "instanceUUID": "2",
        "name": "datastore2",
        "moref": "ds2-2",
        "datastore": ["vm-3", "vm-4"]
    }
]