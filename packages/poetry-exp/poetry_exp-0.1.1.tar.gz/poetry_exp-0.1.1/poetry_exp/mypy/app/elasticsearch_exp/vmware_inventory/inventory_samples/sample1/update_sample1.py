UPDATE_SAMPLE1 = {
   "id": 'd8deb0f7-5822-408d-816b-0bd621271375',  # doc id of vcenter host
   "name": "vcenter1",
   "hosts": [
       {
           "action": "ADD",
           "details": {
               "moref": "host-3",
               "name": "Host3"
           }
       },
       {
           "action": "Remove",
           "details": {
               "moref": "host-2",
               "name": "Host2"
           }
       },
       {
           "action": "Modify",
           "details": {
               "moref": "host-1",
               "name": "Host111"
           }
       }
   ],
   "datastores": [
       {
           "action": "ADD",
           "details": {
               "moref": "ds-5",
               "name": "Datastore5",
               "vms": [

               ],
               "folder": {
                   "moref": "group-s1",
                   "name": "dsFolder1"
               },
               "host": {
                   "moref": "host-1",
                   "name": "Host111"
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
               }
           }
       },
       {
           "action": "Remove",
           "details": {
               "moref": "ds-2"
           }
       }
   ],
   "vms": [
       {
           "action": "ADD",
           "details": {
               "moref": "vm-6",
               "name": "vm6",
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
               }
           }
       },
       {
           "action": "Modify",
           "details": {
               "moref": "vm-3",
               "name": "vm33",
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
                   "moref": "group-2",
                   "name": "vmFolder2"
               },
               "host": {
                   "moref": "host-1",
                   "name": "Host111"
               }
           }
       },
       {
           "action": "Remove",
           "details": {
               "moref": "vm-1"
           }
       }
   ]
}