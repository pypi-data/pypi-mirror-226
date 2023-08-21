import time
from elasticsearch_exp.es_inventory import constants
from elasticsearch_exp.es_inventory import es_const
from elasticsearch_exp.es_inventory.es_enventory_base import ESInventoryBase

from elasticsearch_exp.es_inventory import es_utils
from elasticsearch_exp.es_inventory.inventory_samples.sample1 import update_sample1
from elasticsearch_exp.es_inventory.inventory_samples.sample2 import update_sample2
from elasticsearch_exp.es_inventory.inventory_samples.sample3 import update_sample3
from elasticsearch_exp.es_inventory.inventory_samples.sample4 import update_sample4


class ESInventoryUpdateHelper(ESInventoryBase):
    def __init__(self, vcenter_change_dict):
        super(ESInventoryUpdateHelper, self).__init__(vcenter_change_dict)

        self.added_datacenter_info = dict()
        self.added_cluster_info = dict()
        self.added_esx_info = dict()
        self.added_ds_info = dict()
        self.added_folder_info = dict()

        self.index_obj_info_map = {
            es_const.INDEX_ESXS: self.added_esx_info,
            es_const.INDEX_DATASTORES: self.added_ds_info,
            es_const.INDEX_FOLDERS: self.added_folder_info
        }

    def _get_resource_details(self, resource, moref, instance_uuid=None):
        query_params = {
            "vcenterInfo.id.keyword": [self.vcenter_info['id']],
            "moref.keyword": [moref],
        }
        if instance_uuid:
            query_params.update({"instanceUuid.keyword": instance_uuid})
        query = es_utils.create_multiple_terms_query(query_params)
        return es_utils.get_by_query(resource, query)

    def _get_object_info(self, index_name, object_details):
        """
        Get elastic search doc info corresponding to vim object
        :param index_name: Name of elastic search index
        :param object_details: A dict containing name and moref
        :return: A dict containing doc id and name
        """
        object_moref = object_details['moref']
        obj_info = self.index_obj_info_map[index_name].get(object_moref)
        if not obj_info:
            es_obj_details = self._get_resource_details(
                index_name, object_moref)
            if es_obj_details:
                obj_info = {
                    'id': es_obj_details[0]['_id'],
                    'name': es_obj_details[0]['_source']['name']
                }
        if obj_info:
            # update the latest name
            obj_info['name'] = object_details['name']
        return obj_info

    def _process_folder_operations_and_build_docs(self, folders):
        pass

    def _process_vm_operations_and_build_docs(self, vms):
        for vm in vms:
            action = vm['action']
            vm_details = vm['details']

            datacenter_info = vm_details.pop('datacenter', None)
            cluster_info = vm_details.pop('cluster', None)

            # Fetch VM's Esx details and perisist/update it
            # in case of remove, it will not be there
            esx_info = None
            vm_esx_details = vm_details.pop('host', None)
            if vm_esx_details:
                esx_info = self._get_object_info(
                    es_const.INDEX_ESXS, vm_esx_details)

            # Fetch VM Datastore details and perisist/update it
            vm_datastores = vm_details.pop('datastores', [])
            ds_info = []
            for ds_detail in vm_datastores:
                ds_info.append(self._get_object_info(
                    es_const.INDEX_DATASTORES, ds_detail))

            # Fetch VM's Folder details and perisist/update it
            vm_folder_details = vm_details.pop('folder', None)
            if vm_folder_details:
                vm_folder_info = self._get_object_info(
                    es_const.INDEX_FOLDERS, vm_folder_details)
                if vm_folder_info is None and\
                        vm_folder_details['name'] == 'vm':
                    vm_folder_info =  constants.VMWARE_ROOT_FOLDER_INFO

            es_vm_details = self._get_resource_details(
                constants.RESOURCE_VM, vm_details['moref']
            )
            msg = 'Object: VM, Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_vm_details else False)
            print(msg)

            vm_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info,
                'clusterInfo': cluster_info,
                'dsInfo': ds_info,
                'esxInfo': esx_info,
                'folderInfo': vm_folder_info
            })

            if action == 'ADD':
                if es_vm_details:
                    self.bulk_docs.append(es_utils.build_index_details(
                        es_const.INDEX_VMS,
                        es_vm_details[0]['_id'], es_const.UPDATE, retry=True
                    ))
                    self.bulk_docs.append({"doc": vm_details})
                else:
                    vm_id = es_utils.generate_new_doc_id()
                    self.bulk_docs.append(es_utils.build_index_details(
                        es_const.INDEX_VMS,
                        vm_id, es_const.INDEX,
                    ))
                    self.bulk_docs.append(vm_details)
            elif action == 'Remove' and es_vm_details:
                self.bulk_docs.append(es_utils.build_index_details(
                    es_const.INDEX_VMS,
                    es_vm_details[0]['_id'], es_const.DELETE
                ))
            elif action == 'Modify':
                self.bulk_docs.append(es_utils.build_index_details(
                    es_const.INDEX_VMS,
                    es_vm_details[0]['_id'], es_const.UPDATE, retry=True
                ))
                self.bulk_docs.append({"doc": vm_details})

    def _process_datastore_operations_and_build_docs(self, datastores):
        for datastore in datastores:
            action = datastore['action']
            ds_details = datastore['details']

            datacenter_info = ds_details.pop('datacenter', None)
            cluster_info = ds_details.pop('cluster', None)

            # Fetch Datastore ESX details and persists/update it
            esx_info = []
            ds_esxs = ds_details.pop('host', [])
            for ds_esx in ds_esxs:
                esx_info.append(self._get_object_info(
                    es_const.INDEX_ESXS, ds_esx))

            # Fetch Datastore's folder details and persists/update it
            folder_info = None
            ds_folder_details = ds_details.pop('folder', None)
            if ds_folder_details:
                folder_info = self._get_object_info(
                    es_const.INDEX_FOLDERS, ds_folder_details)
                if folder_info is None and \
                        ds_folder_details['name'] == 'datastore':
                    folder_info = constants.VMWARE_ROOT_FOLDER_INFO

            ds_details.pop('vms', None)
            ds_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info,
                'clusterInfo': cluster_info,
                'esxInfo': esx_info,
                'folderInfo': folder_info
            })

            es_ds_details = self._get_resource_details(
                constants.RESOURCE_DATASTORE, ds_details['moref']
            )
            msg = 'Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_ds_details else False)
            print(msg)

            if action == 'ADD':
                if es_ds_details:
                    self.bulk_docs.append(es_utils.build_index_details(
                        es_const.INDEX_DATASTORES,
                        es_ds_details[0]['_id'], es_const.UPDATE, retry=True
                    ))
                    self.bulk_docs.append({"doc": ds_details})
                else:
                    if not self.added_ds_info.get(
                            ds_details['moref']):
                        ds_id = es_utils.generate_new_doc_id()
                        self.bulk_docs.append(es_utils.build_index_details(
                            es_const.INDEX_DATASTORES,
                            ds_id, es_const.INDEX
                        ))
                        self.bulk_docs.append(ds_details)
                        self.added_ds_info[ds_details['moref']] = {
                            'id': ds_id,
                            'name': ds_details['name']
                        }
            elif action == 'Remove' and es_ds_details:
                self.bulk_docs.append(es_utils.build_index_details(
                    es_const.INDEX_DATASTORES,
                    es_ds_details[0]['_id'], es_const.DELETE
                ))
            elif action == 'Modify' and es_ds_details:
                self.bulk_docs.append(es_utils.build_index_details(
                    es_const.INDEX_DATASTORES,
                    es_ds_details[0]['_id'], es_const.UPDATE, retry=True
                ))
                self.bulk_docs.append({"doc": ds_details})

    def _process_host_operations_and_build_docs(self, hosts):
        for esx in hosts:
            print(esx)
            action = esx['action']
            esx_details = esx['details']
            esx_details.pop('datastores', None)

            datacenter_info = esx_details.pop('datacenter', None)
            cluster_info = esx_details.pop('cluster', None)

            esx_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info,
                'clusterInfo': cluster_info
            })
            es_esx_details = self._get_resource_details(
                constants.RESOURCE_ESX, esx_details['moref']
            )

            msg = 'Object: Host, Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_esx_details else False)
            print(msg)
            if action == 'ADD':
                if es_esx_details:
                    self.bulk_docs.append(es_utils.build_index_details(
                        es_const.INDEX_ESXS,
                        es_esx_details[0]['_id'], es_const.UPDATE, retry=True
                    ))
                    self.bulk_docs.append({"doc": esx_details})
                else:
                    if not self.added_esx_info.get(
                            esx_details['moref']):
                        print('Adding host...from host operation : {0}'.format(esx_details))
                        esx_id = es_utils.generate_new_doc_id()
                        self.bulk_docs.append(es_utils.build_index_details(
                            es_const.INDEX_ESXS,
                            esx_id, es_const.INDEX
                        ))
                        self.bulk_docs.append(esx_details)
                        self.added_esx_info[esx_details['moref']] =\
                            {'id': esx_id, 'name': esx_details['name']}
            elif action == 'Remove' and es_esx_details:
                self.bulk_docs.append(es_utils.build_index_details(
                    es_const.INDEX_ESXS,
                    es_esx_details[0]['_id'], es_const.DELETE, retry=True
                ))
            elif action == 'Modify' and es_esx_details:
                self.bulk_docs.append(es_utils.build_index_details(
                    es_const.INDEX_ESXS,
                    es_esx_details[0]['_id'], es_const.UPDATE, retry=True
                ))
                self.bulk_docs.append({"doc": esx_details})

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
        self._update_bulk_docs()
        t2 = time.time()
        print('Time took to process and update inventory change with ES is'
              ' {0} sec'.format(t2 - t1))


def update_inventory(vcenter_changed_dict):
    # Note:
    # event should be sorted by time(older  events should come first)
    es_inventory_update_helper = ESInventoryUpdateHelper(vcenter_changed_dict)
    es_inventory_update_helper.update_inventory()


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