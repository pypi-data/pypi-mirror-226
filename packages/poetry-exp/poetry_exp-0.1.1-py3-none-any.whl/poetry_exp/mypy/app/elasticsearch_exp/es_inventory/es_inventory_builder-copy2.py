import time
from elasticsearch_exp.es_inventory import es_utils
from elasticsearch_exp.es_inventory import constants
from elasticsearch_exp.es_inventory.inventory_samples.sample1 import build_sample1
from elasticsearch_exp.es_inventory.inventory_samples.sample2 import build_sample2
from elasticsearch_exp.es_inventory.inventory_samples.inventory_sample_dict_builder import build_inventory_sample

class ESInventoryBuildHelper:
    def __init__(self, vcenter_dict):
        self.vcenter_dict = vcenter_dict
        self.vcenter_info = {
            'id':  self.vcenter_dict['id'],
            'name':  self.vcenter_dict['name']
        }
        self.bulk_docs = []
        self.folder_moref_map = dict()

    def _build_folder_docs(self, folder_details):
        folder_info = None
        if folder_details:
            folder_info = self.folder_moref_map.get(folder_details['moref'])
            if not folder_info:
                folder_id = es_utils.generate_new_doc_id()
                folder_info = {
                    'id': folder_id,
                    'name': folder_details['name']
                }

                self.folder_moref_map[folder_details['moref']] = folder_info
                self.bulk_docs.append({
                    "index": {"_index": constants.RESOURCE_FOLDER, "_id": folder_id}
                })
                self.bulk_docs.append(folder_details)
        return folder_info

    def build_bulk_docs(self):
        """
        Build the data in following format:
        {"index": {"_index": "poc-esxs", "_id": "02617490-b254-4158-b2f7-4d4934e247cd"}}
        {"moref": "host-1", "name": "Host1", "vcenterInfo": {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df", "name": "vcenter1"}}
        {"index": {"_index": "poc-folders", "_id": "4de275b3-8ca5-4aee-b334-b0782041bf83"}}
        {"moref": "group-s1", "name": "dsFolder1"}
        {"index": {"_index": "poc-datastores", "_id": "6782a57e-a573-4a81-b1d0-b14c38fa4b4e"}}
        {"moref": "ds-1", "name": "Datastore1", "esxInfo": {"id": "02617490-b254-4158-b2f7-4d4934e247cd", "name": "Host1"}, "vcenterInfo": {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df", "name": "vcenter1"}, "folderInfo": {"id": "4de275b3-8ca5-4aee-b334-b0782041bf83", "name": "dsFolder1"}}
        {"index": {"_index": "poc-folders", "_id": "b51f0756-3a93-41a5-a045-662aa9bc3bbf"}}
        {"moref": "group-1", "name": "vmFolder1"}
        {"index": {"_index": "poc-vms", "_id": "aa2043c6-9a40-4967-b0e2-b27fa376a540"}}
        {"moref": "vm-1", "name": "vm1", "dsInfo": [{"id": "6782a57e-a573-4a81-b1d0-b14c38fa4b4e", "name": "Datastore1"}], "vcenterInfo": {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df", "name": "vcenter1"}, "folderInfo": {"id": "b51f0756-3a93-41a5-a045-662aa9bc3bbf", "name": "vmFolder1"}}
        {"index": {"_index": "poc-folders", "_id": "1ad95dee-50ef-452f-aeca-64b18eb91a79"}}
        {"moref": "group-2", "name": "vmFolder2"}
        {"index": {"_index": "poc-vms", "_id": "a91a2c87-daea-4c71-9cd5-297945a4adc3"}}
        {"moref": "vm-3", "name": "vm3", "dsInfo": [{"id": "6782a57e-a573-4a81-b1d0-b14c38fa4b4e", "name": "Datastore1"}], "vcenterInfo": {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df", "name": "vcenter1"}, "folderInfo": {"id": "1ad95dee-50ef-452f-aeca-64b18eb91a79", "name": "vmFolder2"}}
        {"index": {"_index": "poc-datastores", "_id": "74562e68-eee3-4ac0-967d-fc6d488743c0"}}
        {"moref": "ds-2", "name": "Datastore2", "esxInfo": {"id": "02617490-b254-4158-b2f7-4d4934e247cd", "name": "Host1"}, "vcenterInfo": {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df", "name": "vcenter1"}, "folderInfo": {"id": "4de275b3-8ca5-4aee-b334-b0782041bf83", "name": "dsFolder1"}}
        {"index": {"_index": "poc-vms", "_id": "c555fe24-ca51-43ae-b944-e9dc167a027b"}}
        {"moref": "vm-2", "name": "vm2", "dsInfo": [{"id": "74562e68-eee3-4ac0-967d-fc6d488743c0", "name": "Datastore2"}], "vcenterInfo": {"id": "220584f9-35f4-49c5-b8a4-acfb4dafb2df", "name": "vcenter1"}, "folderInfo": {"id": "b51f0756-3a93-41a5-a045-662aa9bc3bbf", "name": "vmFolder1"}}
        {"update": {"_index": "poc-vms", "_id": "a91a2c87-daea-4c71-9cd5-297945a4adc3"}}
        {"doc": {"dsInfo": [{"id": "6782a57e-a573-4a81-b1d0-b14c38fa4b4e", "name": "Datastore1"}, {"id": "74562e68-eee3-4ac0-967d-fc6d488743c0", "name": "Datastore2"}]}}

        """
        vm_ds_map = dict()
        ds_host_map = dict()

        datacenters = self.vcenter_dict.get('datacenters', [])
        if not datacenters:
            print('No datacenters found.')

        for datacenter in datacenters:
            datacenter_id = es_utils.generate_new_doc_id()
            datacenter_info = {
                'id': datacenter_id,
                'name': datacenter['name']
            }
            clusters = datacenter.pop('clusters', [])
            self.bulk_docs.append({"index": {
                "_index": constants.RESOURCE_DATACENTER,
                "_id": datacenter_id}
            })
            datacenter.update({'vcenterInfo': self.vcenter_info})
            self.bulk_docs.append(datacenter)

            for cluster in clusters:
                clusters_id = es_utils.generate_new_doc_id()
                clusters_info = {
                    'id': clusters_id,
                    'name': cluster['name']
                }
                hosts = cluster.pop('hosts', [])
                self.bulk_docs.append({"index": {
                    "_index": constants.RESOURCE_CLUSTERS, "_id": clusters_id
                }})
                cluster.update({
                    'vcenterInfo': self.vcenter_info,
                    'datacenterInfo': datacenter_info
                })
                self.bulk_docs.append(cluster)

                for esx in hosts:
                    esx_id = es_utils.generate_new_doc_id()
                    esx_details = {
                        'id': esx_id,
                        'name': esx['name']
                    }
                    datastores = esx.pop('datastores', [])
                    self.bulk_docs.append({"index": {
                        "_index": constants.RESOURCE_ESX, "_id": esx_id
                    }})
                    esx.update({
                        'vcenterInfo': self.vcenter_info,
                        'datacenterInfo': datacenter_info,
                        'clusterInfo': clusters_info
                    })
                    self.bulk_docs.append(esx)

                    for datastore in datastores:
                        #if ds_host_map[datastore['moref']]:
                        ds_id = es_utils.generate_new_doc_id()
                        ds_info = {
                            'id': ds_id,
                            'name': datastore['name']
                        }
                        vms = datastore.pop('vms', [])
                        ds_folder_info = datastore.pop('folder', None)
                        folder_info = self._build_folder_docs(ds_folder_info)

                        self.bulk_docs.append({"index": {
                            "_index": constants.RESOURCE_DATASTORE,
                            "_id": ds_id}
                        })
                        datastore.update({
                            'datacenterInfo': datacenter_info,
                            'clusterInfo': clusters_info,
                            'esxInfo': esx_details,
                            'vcenterInfo': self.vcenter_info,
                            'folderInfo': folder_info
                        })
                        self.bulk_docs.append(datastore)

                        for vm in vms:
                            vm_folder_info = vm.pop('folder', None)
                            folder_info = self._build_folder_docs(vm_folder_info)

                            if vm_ds_map.get(vm['moref']):
                                # print('VM moref : {0}  found, updating'
                                #       ' existing one'.format(vm['moref']))
                                # already added to persist, need to update only dsInfo
                                vm_details = vm_ds_map.get(vm['moref'])
                                vm_ds_info = vm_details['dsInfo']
                                vm_ds_info.append(ds_info)
                                self.bulk_docs.append({
                                    "update": {
                                        "_index": constants.RESOURCE_VM,
                                        "_id": vm_details['id'],
                                    }
                                })
                                self.bulk_docs.append({
                                    "doc": {
                                        'dsInfo': vm_ds_info
                                    }
                                })
                            else:
                                # print('VM moref : {0} not found, adding new'.format(
                                #     vm['moref']))
                                vm_id = es_utils.generate_new_doc_id()
                                vm_ds_map[vm['moref']] = {
                                    'dsInfo': [ds_info],
                                    'id': vm_id
                                }
                                self.bulk_docs.append({
                                    "index": {
                                        "_index": constants.RESOURCE_VM,
                                        "_id": vm_id
                                    }
                                })
                                vm.update({
                                    'vcenterInfo': self.vcenter_info,
                                    'datacenterInfo': datacenter_info,
                                    'clusterInfo': clusters_info,
                                    'esxInfo': esx_details,
                                    'dsInfo': [ds_info],
                                    'folderInfo': folder_info
                                })
                                self.bulk_docs.append(vm)

    def build_inventory(self):
        t1 = time.time()
        self.build_bulk_docs()
        t2 = time.time()
        print('Time took to build bulk docs is {0} sec'.format(t2 - t1))
        es_utils.update_bulk_docs(self.bulk_docs)
        t2 = time.time()
        print('Total time build and update bulk docs is {0} sec'.format(t2 - t1))


def build_es_inventory(vcenter_dict):
    es_inventry_builder = ESInventoryBuildHelper(vcenter_dict)
    es_inventry_builder.build_inventory()


def delete_es_inventory():
    es_utils.delete_indices(
        [constants.RESOURCE_DATACENTER,
         constants.RESOURCE_CLUSTERS,
         constants.RESOURCE_ESX,
         constants.RESOURCE_DATASTORE,
         constants.RESOURCE_VM,
         constants.RESOURCE_FOLDER
         ]
    )


if __name__ == '__main__':
    vcenter_dict = build_sample2.BUILD_SAMPLE2
    #build_es_inventory(vcenter_dict)
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
    vcenter_dict = build_inventory_sample(
        inventory_obj_count=INVENTORY_OBJ_COUNT)
    build_es_inventory(vcenter_dict)


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


