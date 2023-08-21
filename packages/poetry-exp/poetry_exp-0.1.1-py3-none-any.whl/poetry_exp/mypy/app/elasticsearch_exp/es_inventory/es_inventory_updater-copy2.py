import time
from elasticsearch_exp.es_inventory import constants
from elasticsearch_exp.es_inventory import es_utils
from elasticsearch_exp.es_inventory.inventory_samples.sample1 import update_sample1
from elasticsearch_exp.es_inventory.inventory_samples.sample2 import update_sample2


class ESInventoryUpdateHelper:
    def __init__(self, vcenter_change_dict):
        self.vcenter_dict = vcenter_change_dict
        self.vcenter_info = {
            'id':  self.vcenter_dict['id'],
            'name':  self.vcenter_dict['name']
        }
        self.bulk_docs = []
        self.added_datacenter_info = dict()
        self.added_cluster_info = dict()
        self.added_esx_info = dict()
        self.added_ds_info = dict()
        self.added_folder_info = dict()

    def _get_resource_details(self, resource, moref, instance_uuid=None):
        query_params = {
            "vcenterInfo.id.keyword": [self.vcenter_info['id']],
            "moref.keyword": [moref],
        }
        if instance_uuid:
            query_params.update({"instanceUuid.keyword": instance_uuid})
        query = es_utils.create_multiple_terms_query(query_params)
        return es_utils.get_by_query(resource, query)

    def _build_datacenter_docs(self, datacenter_details):
        datacenter_info = None
        if datacenter_details:
            datacenter_details.update({'vcenterInfo': self.vcenter_info})
            es_vm_datacenter_details = self._get_resource_details(
                constants.RESOURCE_DATACENTER, datacenter_details['moref']
            )

            if es_vm_datacenter_details:
                datacenter_id = es_vm_datacenter_details[0]['_id']
                datacenter_info = {
                    'id': datacenter_id,
                    'name': datacenter_details['name']
                }
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_DATACENTER,
                    "_id": datacenter_id}
                })
                self.bulk_docs.append({"doc": datacenter_details})
            else:
                datacenter_info = self.added_datacenter_info.get(
                        datacenter_details['moref'])
                if not datacenter_info:
                    datacenter_id = es_utils.generate_new_doc_id()
                    datacenter_info = {
                        'id': datacenter_id,
                        'name': datacenter_details['name']
                    }
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_DATACENTER,
                        "_id": datacenter_id}
                    })
                    self.bulk_docs.append(datacenter_details)
                    self.added_datacenter_info[datacenter_details['moref']] =\
                        datacenter_info
        return datacenter_info

    def _build_cluster_docs(self, cluster_details, datacenter_info):
        cluster_info = None
        if cluster_details:
            cluster_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info
            })
            es_vm_cluster_details = self._get_resource_details(
                constants.RESOURCE_CLUSTERS, cluster_details['moref']
            )

            if es_vm_cluster_details:
                cluster_id = es_vm_cluster_details[0]['_id']
                cluster_info = {
                    'id': cluster_id,
                    'name': cluster_details['name']
                }
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_CLUSTERS,
                    "_id": cluster_id}
                })
                self.bulk_docs.append({"doc": cluster_details})
            else:
                cluster_info = self.added_cluster_info.get(
                        cluster_details['moref'])
                if not cluster_info:
                    cluster_id = es_utils.generate_new_doc_id()
                    cluster_info = {
                        'id': cluster_id,
                        'name': cluster_details['name']
                    }
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_CLUSTERS,
                        "_id": cluster_id}
                    })
                    self.bulk_docs.append(cluster_details)
                    self.added_cluster_info[cluster_details['moref']] =\
                        cluster_info
        return cluster_info

    def _build_esx_docs(self, esx_details,  datacenter_info, cluster_info):
        esx_info = None
        if esx_details:
            esx_details.pop('datastores', [])
            esx_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info,
                'clusterInfo': cluster_info
            })
            es_vm_esx_details = self._get_resource_details(
                constants.RESOURCE_ESX, esx_details['moref']
            )
            if es_vm_esx_details:
                esx_id = es_vm_esx_details[0]['_id']
                esx_info = {
                    'id': esx_id,
                    'name': esx_details['name']
                }
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_ESX,
                    "_id": esx_id}
                })
                self.bulk_docs.append({"doc": esx_details})
            else:
                esx_info = self.added_esx_info.get(
                        esx_details['moref'])
                if not esx_info:
                    esx_id = es_utils.generate_new_doc_id()
                    esx_info = {
                        'id': esx_id,
                        'name': esx_details['name']
                    }
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_ESX, "_id": esx_id}
                    })
                    self.bulk_docs.append(esx_details)
                    self.added_esx_info[esx_details['moref']] = esx_info

        return esx_info

    def _build_folder_docs(self, folder_details):
        folder_info = None
        if folder_details:
            folder_details.update({'vcenterInfo': self.vcenter_info})
            es_ds_folder_details = self._get_resource_details(
                constants.RESOURCE_FOLDER, folder_details['moref']
            )

            if es_ds_folder_details:
                folder_id = es_ds_folder_details[0]['_id']
                folder_info = {
                    'id':  folder_id,
                    'name': folder_details['name']
                }
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_FOLDER,
                    "_id": folder_id}
                })
                self.bulk_docs.append({"doc": folder_details})
            else:
                folder_info = self.added_folder_info.get(
                        folder_details['moref'])
                if not folder_info:
                    folder_id = es_utils.generate_new_doc_id()
                    folder_info = {
                        'id': folder_id,
                        'name': folder_details['name']
                    }
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_FOLDER,
                        "_id": folder_id}
                    })
                    self.bulk_docs.append(folder_details)
                    self.added_folder_info[folder_details['moref']] =\
                        folder_info

        return folder_info

    def _build_datastore_docs(self, datastores, datacenter_info, cluster_info, esx_info):
        ds_info = []
        if datastores:
            for datastore in datastores:
                ds_folder_details = datastore.pop('folder', None)
                ds_folder_info = self._build_folder_docs(ds_folder_details)

                es_ds_details = self._get_resource_details(
                    constants.RESOURCE_DATASTORE, datastore['moref']
                )
                if es_ds_details:
                    ds_info.append({
                        'id': es_ds_details[0]['_id'],
                        'name': es_ds_details[0]['_source']['name']
                    })
                else:
                    if not self.added_ds_info.get(
                            datastore['moref']):
                        ds_id = es_utils.generate_new_doc_id()
                        datastore.update({
                            'vcenterInfo': self.vcenter_info,
                            'datacenterInfo': datacenter_info,
                            'clusterInfo': cluster_info,
                            'esxInfo': esx_info,
                            'folderInfo': ds_folder_info
                        })
                        self.bulk_docs.append({"index": {
                            "_index": constants.RESOURCE_DATASTORE,
                            "_id": ds_id}
                        })
                        self.bulk_docs.append(datastore)
                        ds_info.append({
                            'id': ds_id,
                            'name': datastore['name']
                        })
                        self.added_ds_info[datastore['moref']] = {
                            'id': ds_id,
                            'name': datastore['name']
                        }
                    else:
                        ds_info.append(
                            self.added_ds_info[datastore['moref']]
                        )
        return ds_info

    def _process_vm_operations_and_build_docs(self, vms):
        for vm in vms:
            action = vm['action']
            vm_details = vm['details']

            vm_datacenter_info = vm_details.pop('datacenter', None)
            datacenter_info = self._build_datacenter_docs(vm_datacenter_info)

            vm_cluster_info = vm_details.pop('cluster', None)
            cluster_info = self._build_cluster_docs(vm_cluster_info, datacenter_info)

            # Fetch VM's Esx details and perisist/update it
            # in case of remove, it will not be there
            vm_esx_details = vm_details.pop('host', None)
            esx_info = self._build_esx_docs(vm_esx_details, datacenter_info, cluster_info)

            # Fetch VM Datastore details and perisist/update it
            vm_datastores = vm_details.pop('datastores', [])
            ds_info = self._build_datastore_docs(vm_datastores, datacenter_info, cluster_info, esx_info)

            # Fetch VM's Folder details and perisist/update it
            vm_folder_details = vm_details.pop('folder', None)
            vm_folder_info = self._build_folder_docs(vm_folder_details)

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
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_VM,
                        "_id": es_vm_details[0]['_id']}
                    })
                    self.bulk_docs.append({"doc": vm_details})
                else:
                    vm_id = es_utils.generate_new_doc_id()
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_VM,
                        "_id": vm_id}
                    })
                    self.bulk_docs.append(vm_details)
            elif action == 'Remove' and es_vm_details:
                self.bulk_docs.append({"delete": {
                    "_index": constants.RESOURCE_VM,
                    "_id": es_vm_details[0]['_id']}
                })
            elif action == 'Modify':
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_VM,
                    "_id": es_vm_details[0]['_id']}
                })
                self.bulk_docs.append({"doc": vm_details})

    def _process_datastore_operations_and_build_docs(self, datastores):
        for datastore in datastores:
            action = datastore['action']
            ds_details = datastore['details']

            ds_datacenter_info = ds_details.pop('datacenter', None)
            datacenter_info = self._build_datacenter_docs(ds_datacenter_info)

            ds_cluster_info = ds_details.pop('cluster', None)
            cluster_info = self._build_cluster_docs(ds_cluster_info, datacenter_info)

            # Fetch Datastore ESX details and persists/update it
            ds_esx_details = ds_details.pop('host', None)
            esx_info = self._build_esx_docs(ds_esx_details, datacenter_info, cluster_info)

            # Fetch Datastore's folder details and persists/update it

            ds_folder_details = ds_details.pop('folder', None)
            ds_folder_info = self._build_folder_docs(ds_folder_details)

            ds_details.pop('vms', None)
            ds_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info,
                'clusterInfo': cluster_info,
                'esxInfo': esx_info,
                'folderInfo': ds_folder_info
            })

            es_ds_details = self._get_resource_details(
                constants.RESOURCE_DATASTORE, ds_details['moref']
            )
            msg = 'Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_ds_details else False)
            print(msg)

            if action == 'ADD':
                if es_ds_details:
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_DATASTORE,
                        "_id": es_ds_details[0]['_id']}
                    })
                    self.bulk_docs.append({"doc": ds_details})
                else:
                    if not self.added_ds_info.get(
                            ds_details['moref']):
                        ds_id = es_utils.generate_new_doc_id()
                        self.bulk_docs.append({"index": {
                            "_index": constants.RESOURCE_DATASTORE,
                            "_id": ds_id}
                        })
                        self.bulk_docs.append(ds_details)
                        self.added_ds_info[ds_details['moref']] = {
                            'id': ds_id,
                            'name': ds_details['name']
                        }
            elif action == 'Remove' and es_ds_details:
                self.bulk_docs.append({"delete": {
                    "_index": constants.RESOURCE_DATASTORE,
                    "_id": es_ds_details[0]['_id']}
                })
            elif action == 'Modify' and es_ds_details:
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_DATASTORE,
                    "_id": es_ds_details[0]['_id']}
                })
                self.bulk_docs.append({"doc": ds_details})

    def _process_host_operations_and_build_docs(self, hosts):
        for esx in hosts:
            print(esx)
            action = esx['action']
            esx_details = esx['details']
            esx_details.pop('datastores', None)

            esx_datacenter_info = esx_details.pop('datacenter', None)
            datacenter_info = self._build_datacenter_docs(esx_datacenter_info)

            esx_cluster_info = esx_details.pop('cluster', None)
            cluster_info = self._build_cluster_docs(esx_cluster_info, datacenter_info)

            esx_details.update({
                'vcenterInfo': self.vcenter_info,
                'datacenterInfo': datacenter_info,
                'clusterInfo': cluster_info
            })
            es_esx_details = self._get_resource_details(
                constants.RESOURCE_ESX, esx_details['moref']
            )
            print('..from host operation, es_esx_details : {0}'.format(es_esx_details))

            msg = 'Object: Host, Action: {0}, Found ES entry: {1}' \
                  ''.format(action, True if es_esx_details else False)
            print(msg)
            if action == 'ADD':
                if es_esx_details:
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_ESX,
                        "_id": es_esx_details[0]['_id']}
                    })
                    self.bulk_docs.append({"doc": esx_details})
                else:
                    if not self.added_esx_info.get(
                            esx_details['moref']):
                        print('Adding host...from host operation : {0}'.format(esx_details))
                        esx_id = es_utils.generate_new_doc_id()
                        self.bulk_docs.append({"index": {
                            "_index": constants.RESOURCE_ESX,
                            "_id": esx_id}
                        })
                        self.bulk_docs.append(esx_details)
                        self.added_esx_info[esx_details['moref']] =\
                            {'id': esx_id, 'name': esx_details['name']}
            elif action == 'Remove' and es_esx_details:
                self.bulk_docs.append({"delete": {
                    "_index": constants.RESOURCE_ESX,
                    "_id": es_esx_details[0]['_id']}
                })
            elif action == 'Modify' and es_esx_details:
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_ESX,
                    "_id": es_esx_details[0]['_id']}
                })
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
        vms = self.vcenter_dict.get('vms', [])
        if vms:
            self._process_vm_operations_and_build_docs(vms)
        else:
            print('No vms found to update ES inventory.')

        datastores = self.vcenter_dict.get('datastores', [])
        if datastores:
            self._process_datastore_operations_and_build_docs(datastores)
        else:
            print('No datastore found to update ES inventory.')

        hosts = self.vcenter_dict.get('hosts', [])
        if hosts:
            self._process_host_operations_and_build_docs(hosts)
        else:
            print('No hosts found to update ES inventory')

    def update_inventory(self):
        t1 = time.time()
        self._build_bulk_docs()
        es_utils.update_bulk_docs(self.bulk_docs)
        t2 = time.time()
        print('Time took to process and update inventory change with ES is'
              ' {0} sec'.format(t2 - t1))


def update_inventory(vcenter_changed_dict):
    # Note:
    # event should be sorted by time(older  events should come first)
    es_inventory_update_helper = ESInventoryUpdateHelper(vcenter_changed_dict)
    es_inventory_update_helper.update_inventory()


if __name__ == '__main__':
    vcenter_changed_dict = update_sample2.UPDATE_SAMPLE2
    update_inventory(vcenter_changed_dict)


"""
Folders in venter:
Datacenter: following are the child folders of 'Datacenter' folder
   - vm
   - host
   - network
   - datastore
"""