UPDATE_SAMPLE2 = {
   "id": 'd8deb0f7-5822-408d-816b-0bd621271375',  # doc id of vcenter host
   "name": "vcenter1",
   "hosts": [
       {
           "action": "ADD",
           "details": {
               "moref": "host-9",
               "name": "Host9",
               "cluster": {
                   'moref': "domain-c5",
                   'name': 'Cluster5'
               },
               "datacenter": {
                   "moref": "datacenter-3",
                   "name": "Datacenter3"
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
               "moref": "ds-17",
               "name": "Datastore17",
               "vms": [

               ],
               "folder": {
                   "moref": "group-s9",
                   "name": "dsFolder9"
               },
               "host": {
                   "moref": "host-9",
                   "name": "Host9"
               },
               "cluster": {
                   'moref': "domain-c5",
                   'name': 'Cluster5'
               },
               "datacenter": {
                   "moref": "datacenter-3",
                   "name": "Datacenter3"
               }
           }
       },
       {
           "action": "Modify",
           "details": {
               "moref": "ds-1",
               "name": "Datastore111",
               "vms": [
               ],
               "folder": {
                   "moref": "group-s1",
                   "name": "dsFolder1"
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
               "moref": "ds-16"
           }
       }
   ],
   "vms": [
       {
           "action": "ADD",
           "details": {
               "moref": "vm-33",
               "name": "vm33",
               "datastores": [
                   {
                       "moref": "ds-17",
                       "name": "Datastore17",
                       "folder": {
                           "moref": "group-s9",
                           "name": "dsFolder9"
                       }
                   }
               ],
               "folder": {
                   "moref": "group-9",
                   "name": "vmFolder9"
               },
               "host": {
                   "moref": "host-9",
                   "name": "Host9"
               },
               "cluster": {
                   'moref': "domain-c5",
                   'name': 'Cluster5'
               },
               "datacenter": {
                   "moref": "datacenter-3",
                   "name": "Datacenter3"
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
                       "moref": "ds-1",
                       "name": "Datastore111",
                       "folder": {
                           "moref": "group-s1",
                           "name": "dsFolder1"
                       }
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
               "moref": "vm-32"
           }
       }
   ]
}