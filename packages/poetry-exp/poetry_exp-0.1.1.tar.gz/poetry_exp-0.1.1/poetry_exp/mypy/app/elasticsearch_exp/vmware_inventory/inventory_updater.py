import time
from elasticsearch_exp.vmware_inventory import constants
from elasticsearch_exp.vmware_inventory import es_const
from elasticsearch_exp.vmware_inventory.inventory_base import VMWareInventoryBase

from elasticsearch_exp.vmware_inventory import es_utils
from elasticsearch_exp.vmware_inventory.inventory_samples.sample1 import update_sample1
from elasticsearch_exp.vmware_inventory.inventory_samples.sample2 import update_sample2
from elasticsearch_exp.vmware_inventory.inventory_samples.sample3 import update_sample3
from elasticsearch_exp.vmware_inventory.inventory_samples.sample4 import update_sample4


class VMWareInventoryUpdateHelper(VMWareInventoryBase):
    def __init__(self, vcenter_change_dict):
        super(VMWareInventoryUpdateHelper, self).__init__(vcenter_change_dict)

    def _update_vms_ds_info(self, es_ds_details, latest_ds_info):
        """
        Update the dsInfo of all the corresponding VMs
        :param es_ds_details: Elastic search version of DS
        :param latest_ds_info: Dict containing latest DS properties
        :return:
        """
        if latest_ds_info['name'] != es_ds_details[0]['_source']['name']:
            # update all the referenced vm's docs
            ds_id = es_ds_details[0]['_id']
            query = es_utils.create_multiple_terms_query({
                es_const.HYPERVISOR_MANAGER_INFO + ".id.keyword":
                    [self.vcenter_info['id']],
                es_const.DATASTORES_INFO + ".id.keyword": [ds_id]
            })
            vms = es_utils.get_by_query(es_const.INDEX_VIRTUAL_MACHINES, query)
            for vm in vms:
                vm_id = vm['_id']
                vm_datastores = vm['_source'][es_const.DATASTORES_INFO]
                updated_ds_info = []
                for vm_datastore in vm_datastores:
                    if vm_datastore['id'] == ds_id:
                        updated_ds_info.append({
                            'id': ds_id,
                            'name': latest_ds_info['name']
                        })
                    else:
                        updated_ds_info.append(vm_datastore)

                self._update_document(
                    es_const.INDEX_VIRTUAL_MACHINES,
                    vm_id,
                    {es_const.DATASTORES_INFO: updated_ds_info}
                )
                query = es_utils.create_multiple_terms_query({
                    es_const.VIRTUAL_MACHINE_INFO + ".id.keyword": [vm_id],
                    es_const.DATASTORE_INFO + ".id.keyword": [ds_id]
                })
                vmdks = es_utils.get_by_query(es_const.INDEX_VIRTUAL_DISKS, query)
                self._update_vmdks_ds_info(vmdks, ds_id, latest_ds_info)

    def _update_vmdks_ds_info(self, vmdks, ds_id, latest_ds_info):
        """
        Update the dsInfo of all the given vmdks
        :param vmdks: Elastic search version of vmdks
        :param latest_ds_info: Dict containing latest DS properties
        :return:
        """
        for vmdk in vmdks:
            vmdk_id = vmdk['_id']
            vmdk_ds_info = vmdk['_source'][es_const.DATASTORE_INFO]
            if vmdk_ds_info['id'] == ds_id and\
                    vmdk_ds_info['name'] != latest_ds_info['name']:
                self._update_document(
                    es_const.INDEX_VIRTUAL_DISKS,
                    vmdk_id,
                    {es_const.DATASTORE_INFO:
                        {'id': ds_id, 'name': latest_ds_info['name']}
                    }
                )

    def _update_vms_esx_info(self, es_esx_details, latest_esx_info):
        """
        Update the esxInfo of all the corresponding vms
        :param es_esx_details:
        :param latest_esx_info:
        :return:
        """
        if latest_esx_info['name'] != es_esx_details[0]['_source']['name']:
            # update all the referenced vm's docs
            esx_id = es_esx_details[0]['_id']
            query = es_utils.create_multiple_terms_query({
                es_const.HYPERVISOR_MANAGER_INFO + ".id.keyword":
                    [self.vcenter_info['id']],
                es_const.HYPERVISOR_HOST_INFO + ".id.keyword": [esx_id]
            })
            vms = es_utils.get_by_query(es_const.INDEX_VIRTUAL_MACHINES, query)
            for vm in vms:
                vm_id = vm['_id']
                hypervisor_host_info = {
                    'id': esx_id,
                    'name': latest_esx_info['name']
                }
                self._update_document(
                    es_const.INDEX_VIRTUAL_MACHINES,
                    vm_id,
                    {es_const.HYPERVISOR_HOST_INFO: hypervisor_host_info}
                )

    def _update_ds_esx_info(self, es_host_details, latest_host_info):
        """
        Update the esxInfo of all the corresponding datastores
        :param es_host_details:
        :param latest_host_info:
        :return:
        """
        if latest_host_info['name'] != es_host_details[0]['_source']['name']:
            # update all the referenced vm's docs
            query = es_utils.create_multiple_terms_query({
                es_const.HYPERVISOR_MANAGER_INFO + ".id.keyword":
                    [self.vcenter_info['id']],
                es_const.HYPERVISOR_HOSTS_INFO + ".id.keyword":
                    [es_host_details[0]['_id']]
            })
            datastores = es_utils.get_by_query(es_const.INDEX_DATASTORES, query)
            for datastore in datastores:
                ds_id = datastore['_id']
                hypervisor_hosts = datastore['_source'][es_const.HYPERVISOR_HOSTS_INFO]
                updated_hosts_info = []
                for ds_esx in hypervisor_hosts:
                    if ds_esx['id'] == es_host_details[0]['_id']:
                        updated_hosts_info.append({
                            'id': es_host_details[0]['_id'],
                            'name': latest_host_info['name']
                        })
                    else:
                        updated_hosts_info.append(ds_esx)
                self._update_document(
                    es_const.INDEX_DATASTORES,
                    ds_id,
                    {es_const.HYPERVISOR_HOSTS_INFO: updated_hosts_info}
                )

    def _process_folder_operations_and_build_docs(self, folders):
        pass

    def _process_vm_operations_and_build_docs(self, vms):
        for vm in vms:
            print(vm)
            action = vm['action']
            vm_details = vm['details']

            datacenter_info = vm_details.pop('datacenter', None)
            cluster_info = vm_details.pop('cluster', None)

            # Fetch VM's Esx details and perisist/update it
            # in case of remove, it will not be there
            hypervisor_host_info = None
            vm_host_moref = vm_details.pop('host', None)
            if vm_host_moref:
                hypervisor_host_info = self._get_object_info(
                    es_const.INDEX_HYPERVISOR_HOSTS, vm_host_moref)

            # Fetch VM Datastore details and perisist/update it
            vm_datastores = vm_details.pop('datastores', [])
            datastores_info = []
            for ds_moref in vm_datastores:
                datastores_info.append(self._get_object_info(
                    es_const.INDEX_DATASTORES, ds_moref))

            # Fetch VM's Folder details
            folder_info = None
            vm_folder_moref = vm_details.pop('folder', None)
            if vm_folder_moref:
                folder_info = self._get_object_info(
                    es_const.INDEX_FOLDERS, vm_folder_moref)

            es_vm_details = self._get_resource_details(
                es_const.INDEX_VIRTUAL_MACHINES, vm_details['moref']
            )
            msg = 'Object: VM, Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_vm_details else False)
            print(msg)

            if action == 'ADD':
                if es_vm_details:
                    self._update_vm(
                        es_vm_details[0]['_id'], vm_details, datacenter_info,
                        cluster_info, hypervisor_host_info, datastores_info,
                        folder_info
                    )
                else:
                    self._add_vm(vm_details, datacenter_info, cluster_info,
                                 hypervisor_host_info, datastores_info, folder_info)
            elif action == 'Remove' and es_vm_details:
                self._delete_vm(es_vm_details[0]['_id'])
            elif action == 'Modify' and es_vm_details:
                self._update_vm(
                    es_vm_details[0]['_id'], vm_details, datacenter_info,
                    cluster_info, hypervisor_host_info, datastores_info,
                    folder_info
                )

    def _delete_vm(self, vm_id):
        self._delete_document(
            es_const.INDEX_VIRTUAL_MACHINES,
            vm_id
        )
        # Find and delete vmdks
        es_vmdks = self._get_vmdks_by_vm_id(vm_id)
        for vmdk in es_vmdks:
            self._delete_document(
                es_const.INDEX_VIRTUAL_DISKS,
                vmdk['_id']
            )

    def _update_vm(self, vm_id, vm_properties, datacenter_info, cluster_info,
                   hypervisor_host_info, datastores_info, folder_info):
        vm_properties.update({
            es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info,
            es_const.DATACENTER_INFO: datacenter_info,
            es_const.CLUSTER_INFO: cluster_info,
            es_const.DATASTORES_INFO: datastores_info,
            es_const.HYPERVISOR_HOST_INFO: hypervisor_host_info,
            es_const.FOLDER_INFO: folder_info
        })
        vmdks = vm_properties.pop('vmdks')
        self._update_document(
            es_const.INDEX_VIRTUAL_MACHINES,
            vm_id,
            vm_properties
        )
        vm_info = {
            'id': vm_id,
            'name': vm_properties['name']
        }
        self._update_vm_vmdks(vmdks, vm_info)

    def _get_vmdks_by_vm_id(self, vm_id):
        query = es_utils.create_multiple_terms_query({
            es_const.VIRTUAL_MACHINE_INFO + ".id.keyword": [vm_id]
        })
        return es_utils.get_by_query(es_const.INDEX_VIRTUAL_DISKS, query)

    def _update_vm_vmdks(self, vmdks, vm_info):

        es_vmdks = self._get_vmdks_by_vm_id(vm_info['id'])
        existing_disk_ids = {vmdk['_source']['diskObjectId']: vmdk['_id']
                             for vmdk in es_vmdks}

        for vmdk in vmdks:
            ds_moref = vmdk.pop('datastore')
            ds_info = self._get_object_info(es_const.INDEX_DATASTORES, ds_moref)
            if vmdk['diskObjectId'] in existing_disk_ids:
                # Disk already exists, just update the properties
                vmdk[es_const.DATASTORE_INFO] = ds_info
                self._update_document(
                    es_const.INDEX_VIRTUAL_DISKS,
                    existing_disk_ids[vmdk['diskObjectId']],
                    vmdk
                )
                existing_disk_ids.pop(vmdk['diskObjectId'])
            else:
                self._add_vmdk(vmdk, ds_info, vm_info)

        # Remove the old disks
        for vmdk_id in existing_disk_ids.values():
            self._delete_document(es_const.INDEX_VIRTUAL_DISKS, vmdk_id)

    def _process_datastore_operations_and_build_docs(self, datastores):
        for datastore in datastores:
            action = datastore['action']
            ds_details = datastore['details']

            datacenter_info = ds_details.pop('datacenter', None)
            cluster_info = ds_details.pop('cluster', None)

            # Fetch Datastore ESX details and persists/update it
            hypervisor_hosts_info = []
            hosts_moref = ds_details.pop('host', [])
            for host_moref in hosts_moref:
                hypervisor_hosts_info.append(self._get_object_info(
                    es_const.INDEX_HYPERVISOR_HOSTS, host_moref))

            # Fetch Datastore's folder details and persists/update it
            folder_info = None
            ds_folder_moref = ds_details.pop('folder', None)
            if ds_folder_moref:
                folder_info = self._get_object_info(
                    es_const.INDEX_FOLDERS, ds_folder_moref)

            ds_details.update({
                es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info,
                es_const.DATACENTER_INFO: datacenter_info,
                es_const.CLUSTER_INFO: cluster_info,
                es_const.HYPERVISOR_HOSTS_INFO: hypervisor_hosts_info,
                es_const.FOLDER_INFO: folder_info
            })

            es_ds_details = self._get_resource_details(
                es_const.INDEX_DATASTORES, ds_details['moref']
            )
            msg = 'Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_ds_details else False)
            print(msg)

            if action == 'ADD':
                if es_ds_details:
                    self._update_datastore(es_ds_details, ds_details)
                else:
                    if not self.cached_datastores_info.get(
                            ds_details['moref']):
                        self._add_datastore(
                            ds_details, datacenter_info, cluster_info,
                            hypervisor_hosts_info, folder_info
                        )
            elif action == 'Remove' and es_ds_details:
                self._delete_document(es_const.INDEX_DATASTORES, es_ds_details[0]['_id'])
            elif action == 'Modify' and es_ds_details:
                self._update_datastore(es_ds_details, ds_details)

    def _update_datastore(self, es_ds_details, ds_properties):
        self._update_document(
            es_const.INDEX_DATASTORES,
            es_ds_details[0]['_id'],
            ds_properties
        )
        self.cached_datastores_info[ds_properties['moref']] = {
            'id': es_ds_details[0]['_id'],
            'name': ds_properties['name']
        }
        self._update_vms_ds_info(es_ds_details, ds_properties)

    def _process_host_operations_and_build_docs(self, hosts):
        for hypervisor_host in hosts:
            action = hypervisor_host['action']
            host_details = hypervisor_host['details']

            datacenter_info = host_details.pop('datacenter', None)
            cluster_info = host_details.pop('cluster', None)

            host_details.update({
                es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info,
                es_const.DATACENTER_INFO: datacenter_info,
                es_const.CLUSTER_INFO: cluster_info
            })
            es_host_details = self._get_resource_details(
                es_const.INDEX_HYPERVISOR_HOSTS, host_details['moref']
            )

            msg = 'Object: Host, Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_host_details else False)
            print(msg)
            if action == 'ADD':
                if es_host_details:
                    self._update_hypervisor_host(es_host_details, host_details)
                else:
                    if not self.cached_hypervisor_hosts_info.get(
                            host_details['moref']):
                       self._add_hypervisor_host(
                           host_details, datacenter_info, cluster_info
                       )
            elif action == 'Remove' and es_host_details:
                self._delete_document(
                    es_const.INDEX_HYPERVISOR_HOSTS,
                    es_host_details[0]['_id']
                )
            elif action == 'Modify' and es_host_details:
                self._update_hypervisor_host(es_host_details, host_details)

    def _update_hypervisor_host(self, es_host_details, host_properties):
        host_id = es_host_details[0]['_id']
        self._update_document(
            es_const.INDEX_HYPERVISOR_HOSTS, host_id,
            host_properties
        )
        self.cached_hypervisor_hosts_info[host_properties['moref']] = {
            'id': es_host_details[0]['_id'],
            'name': host_properties['name']
        }
        self._update_ds_esx_info(es_host_details, host_properties)
        self._update_vms_esx_info(es_host_details, host_properties)

    def _build_bulk_docs(self):
        """
        Build the data in following format:
        {"index": {"_index": "poc-esxs",
         "_id": "5dd77a67-8780-48a0-b160-a562e0d72389"}}
        {"doc": {"moref": "host-1", "name": "Host111", "vcenterInfo": {"id":
         "d8deb0f7-5822-408d-816b-0bd621271375", "name": "vcenter1"}}}

        {"index": {"_index": "poc-vms", "_id":
         "448b1f2b-36d8-48f7-b66e-1da8d9e3e93f"}}
        {"moref": "vm-6", "name": "vm6", "vcenterInfo": {"id":
         "d8deb0f7-5822-408d-816b-0bd621271375", "name": "vcenter1"},
          "dsInfo": [{"id": "2630b98d-5311-4bd3-8881-818b94087d2e",
           "name": "Datastore1"}], "esxInfo": {"name": "Host111",
            "id": "5dd77a67-8780-48a0-b160-a562e0d72389"},
             "folderInfo": {"name": "vmFolder1",
              "id": "d72afc4b-6913-42ba-ba91-79efd133434e"}}
        {"delete": {"_index": "poc-vms", "_id": "4c54fd44-af10-470c-8238-d4a2631d5223"}}

        """

        folders = self.vcenter_dict.get('folders', [])
        if folders:
            self._process_folder_operations_and_build_docs(folders)
        else:
            print('No folders found to update ES inventory.')

        hosts = self.vcenter_dict.get('hosts', [])
        if hosts:
            self._process_host_operations_and_build_docs(hosts)
        else:
            print('No hosts found to update ES inventory')

        datastores = self.vcenter_dict.get('datastores', [])
        if datastores:
            self._process_datastore_operations_and_build_docs(datastores)
        else:
            print('No datastore found to update ES inventory.')

        vms = self.vcenter_dict.get('vms', [])
        if vms:
            self._process_vm_operations_and_build_docs(vms)
        else:
            print('No vms found to update ES inventory.')

    def update_inventory(self):
        t1 = time.time()
        self._build_bulk_docs()
        es_utils.bulk_update(self.bulk_docs)
        t2 = time.time()
        print('Time took to process and update inventory change with ES is'
              ' {0} sec'.format(t2 - t1))
        print(self.cached_datastores_info)


def update_inventory(vcenter_changed_dict):
    # Note:
    # event should be sorted by time(older  events should come first)
    inventory_update_helper = VMWareInventoryUpdateHelper(vcenter_changed_dict)
    inventory_update_helper.update_inventory()


if __name__ == '__main__':
    # vcenter_changed_dict = update_sample2.UPDATE_SAMPLE2
    # update_inventory(vcenter_changed_dict)

    # vcenter_changed_dict = update_sample3.UPDATE_SAMPLE3
    # update_inventory(vcenter_changed_dict)

    vcenter_changed_dict = update_sample4.UPDATE_SAMPLE4
    update_inventory(vcenter_changed_dict)


"""
Folders in venter:
Datacenter: following are the child folders of 'Datacenter' folder
   - vm
   - host
   - network
   - datastore
"""