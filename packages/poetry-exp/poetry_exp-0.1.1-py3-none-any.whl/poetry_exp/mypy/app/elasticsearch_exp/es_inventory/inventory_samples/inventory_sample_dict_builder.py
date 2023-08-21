VCENTER_UUID = 'd8deb0f7-5822-408d-816b-0bd621271375'
VCENTER_NAME = 'vcenter1'

INVENTORY_OBJ_COUNT = {
    "datacenters": {
        "count": 2,
        "vmFolders": {
            "count": 4,
            "subFolders": {
                "count": 2
            }
        },
        "storageFolders": {
            "count": 4,
            "subFolders": {
                "count": 2
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


vm_folder_moref = 0
ds_folder_moref = 0


def build_folders(vm_folder_count, vm_sub_folder_count, folder_type='vm'):
    global vm_folder_moref
    global ds_folder_moref

    vm_folders = []
    for j in range(1, vm_folder_count + 1):
        if folder_type == 'vm':
            vm_folder_moref += 1
        else:
            ds_folder_moref += 1

        if folder_type == 'datastore':
            folder_name = 'dsFolder' + str(j)
            folder_moref = 'group-s' + str(ds_folder_moref)
        else:
            folder_name = 'vmFolder' + str(j)
            folder_moref = 'group-' + str(vm_folder_moref)

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
                ds_folder_moref += 1
                sub_folder_moref = 'group-s' + str(ds_folder_moref)
            else:
                vm_folder_moref += 1
                sub_folder_moref = 'group-' + str(vm_folder_moref)

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
                        "moref": 'group-' + str((vm_folder_moref + 1) if folder_type=='vm' else 's'+str((ds_folder_moref + 1))),
                        "type": folder_type,
                        "parent": {
                            "name": sub_folder_name,
                            "moref": sub_folder_moref
                        },
                        "sub_folder": []
                    }
                ]
            }
            if folder_type=='vm':
                vm_folder_moref += 1
            else:
                ds_folder_moref += 1
            vm_sub_folders.append(vm_sub_folder)

        vm_folder['sub_folder'] = vm_sub_folders
        vm_folders.append(vm_folder)
    return vm_folders

def build_inventory_sample(
        vcenter_id=VCENTER_UUID,
        vcenter_name=VCENTER_UUID,
        inventory_obj_count=INVENTORY_OBJ_COUNT):

    vcenter_dict = {
        "id": vcenter_id,  # doc id of vcenter host
        "name": vcenter_name,
        'datacenters': [],
    }
    ds_moref = 0
    vm_moref = 0
    host_moref = 0
    vm_folder_count = inventory_obj_count['datacenters']['vmFolders']['count']
    vm_sub_folder_count = inventory_obj_count['datacenters']['vmFolders']['subFolders']['count']
    ds_folder_count = inventory_obj_count['datacenters']['storageFolders']['count']
    ds_sub_folder_count = inventory_obj_count['datacenters']['storageFolders']['subFolders']['count']

    datacenter_count = inventory_obj_count['datacenters']['count']
    host_count = inventory_obj_count['datacenters']['hosts']['count']
    datastore_count = inventory_obj_count['datacenters']['hosts']['datastores']['count']
    vm_count = inventory_obj_count['datacenters']['hosts']['datastores']["vms"]['count']

    datcenter_details = []
    for i in range(1, datacenter_count+1):
        datacenter = {
            "name": 'Datacenter' + str(i),
            "moref": 'datacenter-' + str(i),
            'folders': [],
            'hosts': []
        }

        vm_folders = build_folders(vm_folder_count, vm_sub_folder_count)
        datacenter['folders'].extend(vm_folders)
        ds_folders = build_folders(ds_folder_count, ds_sub_folder_count, folder_type='datastore')
        datacenter['folders'].extend(ds_folders)
        hosts = []
        for k in range(1, host_count+1):
            host_moref += 1
            host = {
                "name": 'Host' + str(host_moref),
                "moref": 'host-' + str(host_moref),
                "datastores": [],
                "cluster": {
                    "name": "Cluster" + str(i),
                    "moref": "domain-c" + str(i)
                }

            }
            ds_folder = {
                "moref": "group-s" + str(host_moref),
                "name": "dsFolder" + str(host_moref)
            }
            vm_folder = {
                "moref": "group-" + str(host_moref),
                "name": "vmFolder" + str(host_moref)
            }
            datastores = []
            for l in range(1, datastore_count + 1):
                ds_moref +=1
                datastore = {
                    "name": 'Datastore' + str(ds_moref),
                    "moref": 'datastore-' + str(ds_moref),
                    "folder": ds_folder,
                    "vms": []
                }
                vms = []
                for m in range(1, vm_count+1):
                    vm_moref += 1
                    vm = {
                        "name": 'vm' + str(vm_moref),
                        "moref": 'vm-' + str(vm_moref),
                        "folder": vm_folder
                    }
                    vms.append(vm)
                datastore['vms'] = vms
                datastores.append(datastore)
            host['datastores'] = datastores
            hosts.append(host)

        datacenter['hosts'] = hosts

        datcenter_details.append(datacenter)
    vcenter_dict['datacenters'] = datcenter_details

    print(vcenter_dict)
    return vcenter_dict


if __name__ == '__main__':
    build_inventory_sample()
