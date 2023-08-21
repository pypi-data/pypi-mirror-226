import time
from elasticsearch_exp.vmware_inventory import es_utils
from elasticsearch_exp.vmware_inventory import constants
from elasticsearch_exp.vmware_inventory import es_const
from elasticsearch_exp.vmware_inventory.inventory_base import VMWareInventoryBase

from elasticsearch_exp.vmware_inventory.inventory_samples.sample1 \
    import build_sample1
from elasticsearch_exp.vmware_inventory.inventory_samples.sample2 \
    import build_sample2
from elasticsearch_exp.vmware_inventory.inventory_samples.sample3 \
    import build_sample3
from elasticsearch_exp.vmware_inventory.inventory_samples.sample4 \
    import build_sample4

from elasticsearch_exp.vmware_inventory.inventory_samples.inventory_sample_dict_builder \
    import build_inventory_sample


class VMWareInventoryBuildHelper(VMWareInventoryBase):
    def __init__(self, vcenter_dict):
        super(VMWareInventoryBuildHelper, self).__init__(vcenter_dict)

    def _add_folders(self, folders, parent_info, datacenter_info):
        folders_info = []
        for folder in folders:
            folder.pop('parent', None)
            folder.update({
                'parentInfo': parent_info,
                es_const.DATACENTER_INFO: datacenter_info,
                es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info
            })
            folder_id = es_utils.generate_new_doc_id()
            folder['id'] = folder_id
            folder_info = {
                'id': folder_id,
                'name': folder['name']
            }
            folders_info.append(folder_info)

            sub_folders = folder.pop('sub_folder', [])
            self.cached_folders_info[folder['moref']] = folder_info
            sub_folders_info = []
            if sub_folders:
                sub_folders_info.extend(
                    self._add_folders(
                        sub_folders, folder_info, datacenter_info
                    )
                )

            folder['subFolders'] = sub_folders_info
            self._add_document(es_const.INDEX_FOLDERS, folder_id, folder)

        return folders_info

    def _build_bulk_docs(self):
        """
        Build the data in following format:
        {"index": {"_index": "vms", "_id":
        "a91a2c87-daea-4c71-9cd5-297945a4adc3"}}

        {"moref": "vm-3", "name": "vm3",
         "dsInfo": [{"id": "6782a57e-a573-4a81-b1d0-b14c38fa4b4e",
         "name": "Datastore1"}], "vcenterInfo":
         {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df",
         "name": "vcenter1"}, "folderInfo":
         {"id": "1ad95dee-50ef-452f-aeca-64b18eb91a79",
         "name": "vmFolder2"}}

        {"index": {"_index": "datastores",
         "_id": "74562e68-eee3-4ac0-967d-fc6d488743c0"}}

        {"moref": "ds-2", "name": "Datastore2",
         "esxInfo": {"id": "02617490-b254-4158-b2f7-4d4934e247cd",
         "name": "Host1"}, "vcenterInfo":
         {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df",
         "name": "vcenter1"}, "folderInfo":
         {"id": "4de275b3-8ca5-4aee-b334-b0782041bf83",
         "name": "dsFolder1"}}

        """
        datacenters = self.vcenter_dict.get('datacenters', [])
        if not datacenters:
            print('No datacenters found.')
            return

        for datacenter in datacenters:
            datacenter_info = {
                'moref': datacenter['moref'],
                'name': datacenter['name']
            }
            folders = datacenter.pop('folders', [])
            self._add_folders(
                folders,
                constants.VMWARE_ROOT_FOLDER_INFO,
                datacenter_info)

            hosts = datacenter.pop('hosts', [])
            if not hosts:
                print('No hosts found.')
                return

            for hypervisor_host in hosts:
                cluster_info = hypervisor_host.pop('cluster', None)
                datastores = hypervisor_host.pop('datastores', [])
                hypervisor_host_info = self._add_hypervisor_host(
                    hypervisor_host, datacenter_info, cluster_info)

                self._add_datastores(
                    datastores, datacenter_info,
                    cluster_info, hypervisor_host_info
                )

    def _add_datastores(self, datastores, datacenter_info,
                        cluster_info, hypervisor_host):
        for datastore in datastores:
            moref = datastore['moref']
            if self.ds_hypervisor_hosts_map.get(moref):
                # This check is because, one esx may belongs
                # to multiple esx, so that datastore will
                # come multiple times
                ds_details = self.ds_hypervisor_hosts_map[moref]
                hypervisor_hosts_info =\
                    ds_details[es_const.HYPERVISOR_HOSTS_INFO]
                hypervisor_hosts_info.append(hypervisor_host)

                self._update_document(
                    es_const.INDEX_DATASTORES,
                    ds_details['id'],
                    {es_const.HYPERVISOR_HOSTS_INFO: hypervisor_hosts_info}
                )
            else:
                ds_folder_moref = datastore.pop('folder', None)
                folder_info = self._get_object_info(
                    es_const.INDEX_FOLDERS, ds_folder_moref)
                vms = datastore.pop('vms', [])
                ds_info = self._add_datastore(
                    datastore, datacenter_info,
                    cluster_info, [hypervisor_host], folder_info
                )
                self._add_vms(
                    vms, ds_info, datacenter_info,
                    cluster_info, hypervisor_host
                )

    def _add_vms(self, vms, ds_info, datacenter_info,
                 cluster_info, hypervisor_host_info):
        for vm in vms:
            folder_moref = vm.pop('folder', None)
            folder_info = self._get_object_info(
                es_const.INDEX_FOLDERS, folder_moref)

            if self.vm_ds_map.get(vm['moref']):
                # already added to persist,
                # need to update only datastoresInfo
                vm_details = self.vm_ds_map.get(vm['moref'])
                vm_datastores_info = vm_details[es_const.DATASTORES_INFO]
                vm_datastores_info.append(ds_info)

                self._update_document(
                    es_const.INDEX_VIRTUAL_MACHINES,
                    vm_details['id'],
                    {es_const.DATASTORES_INFO: vm_datastores_info}
                )
            else:
                self._add_vm(vm, datacenter_info, cluster_info,
                             hypervisor_host_info, ds_info, folder_info)

    def build_inventory(self):
        t1 = time.time()
        self._build_bulk_docs()
        t2 = time.time()
        print('Time took to build bulk docs is {0} sec'.format(
            t2 - t1))
        self._update_bulk_docs()
        t2 = time.time()
        print('Total time build and update bulk docs is {0} sec'.format(
            t2 - t1))
        print(self.cached_datastores_info)


def build_es_inventory(vcenter_dict):
    inventry_builder = VMWareInventoryBuildHelper(vcenter_dict)
    inventry_builder.build_inventory()


def delete_es_inventory():
    es_utils.delete_indices(
        [es_const.INDEX_HYPERVISOR_HOSTS,
         es_const.INDEX_DATASTORES,
         es_const.INDEX_VIRTUAL_MACHINES,
         es_const.INDEX_FOLDERS,
         es_const.INDEX_VIRTUAL_DISKS
         ]
    )


if __name__ == '__main__':
    vcenter_dict = build_sample2.BUILD_SAMPLE2
    # build_es_inventory(vcenter_dict)
    delete_es_inventory()

    # 2 Datacenter with 2 clusters, each cluster has 2 hosts
    # Total 8 hosts in 4 clusters, each host has 5 datastore
    # total datastore = 40 (8(hosts)*5(datastrore), each datastore has 250 VMS
    # Total VMs = 10k(40(dastore)*250(vms))
    # Total VMs = 20k(40(dastore)*500(vms))

    INVENTORY_OBJ_COUNT = {
        "datacenters": {
            "count": 2,
            "clusters": {
                "count": 2,
                "hosts": {
                    "count": 2,
                    "datastores": {
                        "count": 5,
                        "vms": {
                            "count": 250
                        }
                    }
                }
            }
        }
    }
    # vcenter_dict = build_inventory_sample(
    #     inventory_obj_count=INVENTORY_OBJ_COUNT)
    # build_es_inventory(vcenter_dict)

    # build_es_inventory(build_sample3.BUILD_SAMPLE3)
    build_es_inventory(build_sample4.BUILD_SAMPLE4)

"""

10K VMs build and update time:
Time took to build bulk docs is 0.12734079360961914 sec
Time took to ES bulk update is 2.310126304626465 sec
Total time build and update bulk docs is 2.6580519676208496 sec


20K VMs build and update time:
Time took to build bulk docs is 0.3479282855987549 sec
Time took to ES bulk update is 3.555567502975464 sec
Total time build and update bulk docs is 4.525169372558594 sec
"""
