UPDATE_SAMPLE4 = {
   "id": 'd8deb0f7-5822-408d-816b-0bd621271375',  # doc id of vcenter host
   "name": "vcenter1",
   "folders": [],
   "hosts": [
       {
           "action": "ADD",
           "details": {
               "moref": "host-5",
               "name": "Host5",
               "cluster": {
                   'moref': "domain-c2",
                   'name': 'Cluster2'
               },
               "datacenter": {
                   "moref": "datacenter-2",
                   "name": "Datacenter2"
               }
           }
       },
       {
           "action": "Remove",
           "details": {
               "moref": "host-10",
           }
       },
       {
           "action": "Modify",
           "details": {
               "moref": "host-1",
               "name": "Host111",
               "cluster": {
                   'moref': "domain-c1",
                   'name': 'Cluster1'
               },
               "datacenter": {
                   "moref": "datacenter-1",
                   "name": "Datacenter1"
               }
           }
       }
   ],
   "datastores": [
       {
           "action": "ADD",
           "details": {
               "moref": "datastore-9",
               "name": "Datastore9",
               "folder": "group-s4",
               "host": ["host-4"],
               "cluster": {
                   'moref': "domain-c2",
                   'name': 'Cluster2'
               },
               "datacenter": {
                   "moref": "datacenter-2",
                   "name": "Datacenter2"
               }
           }
       },
       {
           "action": "Modify",
           "details": {
               "moref": "datastore-1",
               "name": "Datastore111",
               "folder": "group-s1",
               "host": ["host-1","host-2"],
               "cluster": {
                   'moref': "domain-c1",
                   'name': 'Cluster1'
               },
               "datacenter": {
                   "moref": "datacenter-1",
                   "name": "Datacenter1"
               }
           }
       },
       {
           "action": "Remove",
           "details": {
               "moref": "datastore-8"
           }
       }
   ],
   "vms": [
       {
           "action": "ADD",
           "details": {
               "moref": "vm-17",
               "name": "vm17",
               "datastores": ["datastore-9"],
               "folder": "group-4",
               "host":"host-4",
               'vmdks': [
                   {
                       'controllerKey': 1000,
                       'controllerType': 'VirtualLsiLogicController',
                       'controllerSharingMode': 'noSharing',
                       'key': 2000,
                       'unitNumber': 0,
                       'diskObjectId': '70-20017',
                       'capacityInBytes': 12884901888,
                       'backingId': '6000C2909afcb47601d120eb136e19c4',
                       'datastore': 'datastore-9',
                       'backingFileInfo': {
                           'type': 'VirtualDiskFlatVer2',
                           'isRDM': False,
                           'vmdkPath': 'Datastore17/vm17.vmdk',
                           'compatibilityMode': None,
                           'vmdkSharingMode': 'sharingNone',
                           'isThinDisk': True,
                           'vmdkDiskMode': 'persistent',
                           'isAccessible': True
                       }
                   }
               ],
               "cluster": {
                   'moref': "domain-c2",
                   'name': 'Cluster2'
               },
               "datacenter": {
                   "moref": "datacenter-2",
                   "name": "Datacenter2"
               }
           }
       },
       {
           "action": "Modify",
           "details": {
               "moref": "vm-1",
               "name": "vm11111",
               "datastores": ["datastore-1"],
               "folder": "group-1",
               "host": "host-1",
               'vmdks': [
                   {
                       'controllerKey': 1000,
                       'controllerType': 'VirtualLsiLogicController',
                       'controllerSharingMode': 'noSharing',
                       'key': 2000,
                       'unitNumber': 0,
                       'diskObjectId': '70-20018',
                       'capacityInBytes': 12884901888,
                       'backingId': '6000C2909afcb47601d120eb136e19c4',
                       'datastore': 'datastore-1',
                       'backingFileInfo': {
                           'type': 'VirtualDiskFlatVer2',
                           'isRDM': False,
                           'vmdkPath': 'Datastore1/vm2.vmdk',
                           'compatibilityMode': None,
                           'vmdkSharingMode': 'sharingNone',
                           'isThinDisk': True,
                           'vmdkDiskMode': 'persistent',
                           'isAccessible': True
                       }
                   }
               ],
               "cluster": {
                   'moref': "domain-c1",
                   'name': 'Cluster1'
               },
               "datacenter": {
                   "moref": "datacenter-1",
                   "name": "Datacenter1"
               }
           }
       },
       {
           "action": "Remove",
           "details": {
               "moref": "vm-16"
           }
       }
   ]
}