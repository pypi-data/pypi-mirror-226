import unittest

class TestInventory(unittest.TestCase):
    """
    This is only a sample Test Class to have a
    quick way if needed to check if any change
    is broken.
    This can be run directly from /usr/lib/python3.6/site-packages
    e.g
    [root@hpedsite-packages]# python3.6 test_inventory_build_update.py
    """

    def setUp(self):
        #self.es_manager = mgr.ESDataManager()
        # this build sample later can be build dynamically for scale testing

        self.vm_folder_moref = 0
        self.ds_folder_moref = 0

    def _get_folder_moref(self, folder_type):
        return 'group-' + str((self.vm_folder_moref + 1)
                              if folder_type == 'vm' else
                              's' + str((self.ds_folder_moref + 1)))

    def _build_folders(self, vm_folder_count, vm_sub_folder_count,
                       folder_type='vm'):

        vm_folders = []
        for j in range(1, vm_folder_count + 1):
            if folder_type == 'vm':
                self.vm_folder_moref += 1
            else:
                self.ds_folder_moref += 1

            if folder_type == 'datastore':
                folder_name = 'dsFolder' + str(j)
                folder_moref = 'group-s' + str(self.ds_folder_moref)
            else:
                folder_name = 'vmFolder' + str(j)
                folder_moref = 'group-' + str(self.vm_folder_moref)

            vm_folder = {
                "name": folder_name,
                "moref": folder_moref,
                "type": folder_type,
                "parent": {
                    "name": folder_type
                },
                "sub_folder": []
            }
            vm_sub_folders = []
            for k in range(1, vm_sub_folder_count + 1):
                sub_folder_name = 'sf' + str(k) + '(' + folder_name + ')'
                if folder_type == 'datastore':
                    self.ds_folder_moref += 1
                    sub_folder_moref = \
                        'group-s' + str(self.ds_folder_moref)
                else:
                    self.vm_folder_moref += 1
                    sub_folder_moref = \
                        'group-' + str(self.vm_folder_moref)

                vm_sub_folder = {
                    "name": sub_folder_name,
                    "moref": sub_folder_moref,
                    "type": folder_type,
                    "parent": {
                        "name": folder_name,
                        "moref": folder_moref
                    },
                    "sub_folder": [
                        {
                            "name": 'ssf1(' + sub_folder_name + ')',
                            "moref": self._get_folder_moref(folder_type),
                            "type": folder_type,
                            "parent": {
                                "name": sub_folder_name,
                                "moref": sub_folder_moref
                            },
                            "sub_folder": []
                        }
                    ]
                }
                if folder_type == 'vm':
                    self.vm_folder_moref += 1
                else:
                    self.ds_folder_moref += 1
                vm_sub_folders.append(vm_sub_folder)

            vm_folder['sub_folder'] = vm_sub_folders
            vm_folders.append(vm_folder)
        return vm_folders

    def _build_inventory_sample(self, inventory_obj_count):
        hypervisor_id = 'd8deb0f7-5822-408d-816b-0bd621271375'
        hypervisor_name = 'vcenter1'
        vcenter_dict = {
            "id": hypervisor_id,
            "name": hypervisor_name,
            'datacenters': [],
        }
        ds_moref = 0
        vm_moref = 0
        vm_instance_uuid = 0
        host_moref = 0
        vmdk_object_id = 0
        datacenters = inventory_obj_count['datacenters']
        vm_folder_count = datacenters['vmFolders']['count']
        vm_sub_folder_count = \
            datacenters['vmFolders']['subFolders']['count']
        ds_folder_count = datacenters['storageFolders']['count']
        ds_sub_folder_count = \
            datacenters['storageFolders']['subFolders']['count']

        datacenter_count = datacenters['count']
        host_count = datacenters['hosts']['count']
        datastore_count = datacenters['hosts']['datastores']['count']
        vm_count = datacenters['hosts']['datastores']["vms"]['count']

        datcenter_details = []
        vms = []
        datastores = []
        hosts = []
        for i in range(1, datacenter_count + 1):
            datacenter = {
                "name": 'Datacenter' + str(i),
                "moref": 'datacenter-' + str(i),
                "folders": [],
                "hosts": [],
                "datastores": [],
                "vms": []
            }

            vm_folders = self._build_folders(
                vm_folder_count, vm_sub_folder_count)
            datacenter['folders'].extend(vm_folders)

            ds_folders = self._build_folders(
                ds_folder_count, ds_sub_folder_count,
                folder_type='datastore')
            datacenter['folders'].extend(ds_folders)

            for k in range(1, host_count + 1):
                host_moref += 1
                host = {
                    "name": 'Host' + str(host_moref),
                    "moref": 'host-' + str(host_moref),
                    "cluster": {
                        "name": "Cluster" + str(i),
                        "moref": "domain-c" + str(i)
                    }

                }
                vm_folder = "group-" + str(host_moref)
                for l in range(1, datastore_count + 1):
                    ds_moref += 1
                    datastore = {
                        "name": 'Datastore' + str(ds_moref),
                        "moref": 'datastore-' + str(ds_moref),
                        "folder": "group-s1"
                    }
                    for m in range(1, vm_count + 1):
                        vm_moref += 1
                        vmdk_object_id += 1
                        vm_instance_uuid += 1
                        vm = {
                            "name": 'vm' + str(vm_moref),
                            "moref": 'vm-' + str(vm_moref),
                            "instanceUuid":
                                "instanceUuid" + str(vm_instance_uuid),
                            "folder": "group-1",
                            "vmdks": [
                                {
                                    "name": "Hard Disk 1",
                                    "controllerKey": 1000,
                                    "controllerType":
                                        "VirtualLsiLogicController",
                                    "controllerSharingMode": "noSharing",
                                    "key": 2000,
                                    "unitNumber": 0,
                                    "diskObjectId":
                                        "70-200" + str(vmdk_object_id),
                                    "capacityInBytes": 12884901888,
                                    "backingId":
                                        "6000C2909afcb47601d120eb136e19c4",
                                    "datastore":
                                        'datastore-' + str(ds_moref),
                                    "backingFileInfo": {
                                        "type": "VirtualDiskFlatVer2",
                                        "isRDM": False,
                                        "vmdkPath":
                                            'Datastore' + str(ds_moref) +
                                            '/' + 'vm' + str(vm_moref) +
                                            '.vmdk',
                                        "compatibilityMode": None,
                                        "vmdkSharingMode": "sharingNone",
                                        "isThinDisk": True,
                                        "vmdkDiskMode": "persistent",
                                        "isAccessible": True}
                                }
                            ]
                        }
                        vms.append(vm)
                    datastores.append(datastore)
                hosts.append(host)

            datacenter['hosts'] = hosts
            datacenter['vms'] = vms
            datacenter['datastores'] = datastores
            datcenter_details.append(datacenter)

        vcenter_dict['datacenters'] = datcenter_details
        return vcenter_dict

    def test_build_inventory(self):
        inventory_obj_count = {
            "datacenters": {
                "count": 2,
                "vmFolders": {
                    "count": 2,
                    "subFolders": {
                        "count": 1
                    }
                },
                "storageFolders": {
                    "count": 2,
                    "subFolders": {
                        "count": 1
                    }
                },
                "hosts": {
                    "count": 2,
                    "datastores": {
                        "count": 2,
                        "vms": {
                            "count": 2
                        }
                    }
                }
            }
        }

        self._build_inventory_sample(inventory_obj_count)


if __name__ == '__main__':
    unittest.main()

