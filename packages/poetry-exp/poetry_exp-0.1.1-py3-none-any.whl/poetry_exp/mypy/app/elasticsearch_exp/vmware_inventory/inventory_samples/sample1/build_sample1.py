BUILD_SAMPLE1 = {
    "id": 'd8deb0f7-5822-408d-816b-0bd621271375', # doc id of vcenter host
    "name": "vcenter1",
    "hosts": [
        {
            "moref": "host-1",
            "name": "Host1",
            "datastores": [
                {
                    "moref": "ds-1",
                    "name": "Datastore1",
                    "folder": {
                        "moref": "group-s1",
                        "name": "dsFolder1"
                    },
                    "vms": [
                        {
                            "moref": "vm-1",
                            "name": "vm1",
                            "folder":{
                                "moref": "group-1",
                                "name": "vmFolder1"
                            }
                        },
                        {
                            "moref": "vm-3",
                            "name": "vm3",
                            "folder": {
                                "moref": "group-2",
                                "name": "vmFolder2"
                            }
                        }
                    ]
                },
                {
                    "moref": "ds-2",
                    "name": "Datastore2",
                    "folder": {
                        "moref": "group-s1",
                        "name": "dsFolder1"
                    },
                    "vms": [
                        {
                            "moref": "vm-2",
                            "name": "vm2",
                            "folder": {
                                "moref": "group-1",
                                "name": "vmFolder1"
                            }
                        },
                        {
                            "moref": "vm-3",
                            "name": "vm3",
                            "folder": {
                                "moref": "group-2",
                                "name": "vmFolder2"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "moref": "host-2",
            "name": "Host2",
            "datastores": [
                {
                    "moref": "ds-3",
                    "name": "Datastore3",
                    "folder": {
                        "moref": "group-s1",
                        "name": "dsFolder1"
                    },
                    "vms": [
                        {
                            "moref": "vm-4",
                            "name": "vm4",
                            "folder": {
                                "moref": "group-1",
                                "name": "vmFolder1"
                            }
                        }
                    ]
                },
                {
                    "moref": "ds-4",
                    "name": "Datastore4",
                    "folder": {
                        "moref": "group-s1",
                        "name": "dsFolder1"
                    },
                    "vms": [
                        {
                            "moref": "vm-5",
                            "name": "vm5",
                            "folder": {
                                "moref": "group-1",
                                "name": "vmFolder1"
                            }
                        }
                    ]
                }
            ]
        }
    ]
}