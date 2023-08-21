UPDATE_SAMPLE4 = {
   "id": 'd8deb0f7-5822-408d-816b-0bd621271375',  # doc id of vcenter host
   "name": "vcenter1",
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
               "folder": {
                   "moref": "group-s4",
                   "name": "sf2(dsFolder1)"
               },
               "host": [
                   {
                       "moref": "host-4",
                       "name": "Host4"
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
               "moref": "datastore-1",
               "name": "Datastore111",
               "vms": [
               ],
               "folder": {
                   "moref": "group-s1",
                   "name": "dsFolder1"
               },
               "host": [
                   {
                       "moref": "host-1",
                       "name": "Host111"
                   },
                   {
                       "moref": "host-2",
                       "name": "Host2"
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
               "datastores": [
                   {
                       "moref": "datastore-9",
                       "name": "Datastore9"
                   }
               ],
               "folder": {
                   "moref": "group-4",
                   "name": "vmFolder4"
               },
               "host": {
                   "moref": "host-4",
                   "name": "Host4"
               },
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
               "datastores": [
                   {
                       "moref": "datastore-1",
                       "name": "Datastore111"
                   }
               ],
               "folder": {
                   "moref": "group-1",
                   "name": "vmFolder1"
               },
               "host": {
                   "moref": "host-1",
                   "name": "Host111"
               },
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