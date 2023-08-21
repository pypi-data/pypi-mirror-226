from elasticsearch_exp.es_inventory import es_utils
from elasticsearch_exp.es_inventory import constants
from elasticsearch_exp.es_inventory.inventory_samples.sample1 import build_sample1
from elasticsearch_exp.es_inventory.inventory_samples.sample2 import build_sample2

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

        hosts = self.vcenter_dict.get('hosts', [])
        if not hosts:
            print('No host found.')

        for esx in hosts:
            esx_id = es_utils.generate_new_doc_id()
            esx_details = {
                'id': esx_id,
                'name': esx['name']
            }
            datastores = esx.pop('datastores', [])
            self.bulk_docs.append({"index": {"_index": constants.RESOURCE_ESX, "_id": esx_id}})
            esx.update({'vcenterInfo': self.vcenter_info})
            self.bulk_docs.append(esx)

            for datastore in datastores:
                ds_id = es_utils.generate_new_doc_id()
                ds_info = {
                    'id': ds_id,
                    'name': datastore['name']
                }
                vms = datastore.pop('vms', [])
                ds_folder_info = datastore.pop('folder', None)
                folder_info = self._build_folder_docs(ds_folder_info)

                self.bulk_docs.append({"index": {"_index": constants.RESOURCE_DATASTORE, "_id": ds_id}})
                datastore.update({
                    'esxInfo': esx_details,
                    'vcenterInfo': self.vcenter_info,
                    'folderInfo': folder_info
                })
                self.bulk_docs.append(datastore)

                for vm in vms:
                    vm_folder_info = vm.pop('folder', None)
                    folder_info = self._build_folder_docs(vm_folder_info)

                    if vm_ds_map.get(vm['moref']):
                        print('VM moref : {0}  found, updating existing one'.format(vm['moref']))
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
                        print('VM moref : {0} not found, adding new'.format(
                            vm['moref']))
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
                            'dsInfo': [ds_info],
                            'vcenterInfo': self.vcenter_info,
                            'esxInfo': esx_details,
                            'folderInfo': folder_info
                        })
                        self.bulk_docs.append(vm)

    def build_inventory(self):
        self.build_bulk_docs()
        es_utils.update_bulk_docs(self.bulk_docs)


def build_es_inventory():
    vcenter_dict = build_sample1.BUILD_SAMPLE1
    es_inventry_builder = ESInventoryBuildHelper(vcenter_dict)
    es_inventry_builder.build_inventory()


def delete_es_inventory():
    es_utils.delete_indices(
        [constants.RESOURCE_ESX,
         constants.RESOURCE_DATASTORE,
         constants.RESOURCE_VM,
         constants.RESOURCE_FOLDER
         ]
    )


if __name__ == '__main__':
    build_es_inventory()
    #delete_es_inventory()
