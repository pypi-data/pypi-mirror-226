VCENTER_UUID = 'd8deb0f7-5822-408d-816b-0bd621271375'
VCENTER_NAME = 'vcenter1'

INVENTORY_OBJ_COUNT = {
    "datacenters": {
        "count": 2,
        "clusters": {
            "count": 2,
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
}

def build_inventory_sample(
        vcenter_id=VCENTER_UUID,
        vcenter_name=VCENTER_UUID,
        inventory_obj_count=INVENTORY_OBJ_COUNT):

    vcenter_dict = {
        "id": vcenter_id,  # doc id of vcenter host
        "name": vcenter_name,
        'datacenters': []
    }

    ds_moref = 0
    vm_moref = 0
    cluster_moref = 0
    host_moref = 0

    datacenter_count = inventory_obj_count['datacenters']['count']
    cluster_count = inventory_obj_count['datacenters']['clusters']['count']
    host_count = inventory_obj_count['datacenters']['clusters']['hosts']['count']
    datastore_count = inventory_obj_count['datacenters']['clusters']['hosts']['datastores']['count']
    vm_count = inventory_obj_count['datacenters']['clusters']['hosts']['datastores']["vms"]['count']

    datcenter_details = []
    for i in range(1, datacenter_count+1):
        datacenter = {
            "name": 'Datacenter' + str(i),
            "moref": 'datacenter-' + str(i),
            'clusters': []
        }
        clusters = []
        for j in range(1, cluster_count+1):
            cluster_moref += 1
            cluster = {
                "name": 'Cluster' + str(cluster_moref),
                "moref": 'domain-c' + str(cluster_moref),
                "hosts": []
            }
            hosts = []
            for k in range(1, host_count+1):
                host_moref += 1
                host = {
                    "name": 'Host' + str(host_moref),
                    "moref": 'host-' + str(host_moref),
                    "datastores": []
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
                        "moref": 'ds-' + str(ds_moref),
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

            cluster['hosts'] = hosts
            clusters.append(cluster)

        datacenter['clusters'] = clusters
        datcenter_details.append(datacenter)
    vcenter_dict['datacenters'] = datcenter_details

    #print(vcenter_dict)
    return vcenter_dict


if __name__ == '__main__':
    build_inventory_sample()
