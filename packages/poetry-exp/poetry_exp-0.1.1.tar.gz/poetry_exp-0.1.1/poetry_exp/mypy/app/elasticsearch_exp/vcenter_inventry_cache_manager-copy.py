from elasticsearch_exp import vcenter_inventroy_const as const
from elasticsearch_exp import es_const
import json
import requests
import json
import time
import uuid

URL = "http://localhost:9200/"
HEADERS = {
    'accept': 'application/json',
    "Content-Type": "application/json"
}

VCENTER_ID = 'd8deb0f7-5822-408d-816b-0bd621271375'

def parse_response(search_response):
    if search_response.status_code == 200:
        documents = search_response.json()['hits']['hits']
        return documents


def get_documents(index_name):
    headers = {
        'accept': 'application/json'
    }
    url = URL + index_name + "/_search?size=10000&seq_no_primary_term=true"
    print(url)
    response = requests.get(
        url, headers=headers)
    print(response) # by default gives only 10 records
    print(response.json())
    return parse_response(response)


def get_document_by_id(index_name, doc_id):
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(
        URL + index_name + "/_doc/"+ str(doc_id), headers=headers)
    #print(response)
    #print(parse_response(response))
    return response.json()


def get_by_query(index_name, query):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    print(query)
    response = requests.get(
        URL + index_name + "/_search?filter_path=hits.hits", data=json.dumps(query), headers=headers)
    print(response)
    #print(parse_response(response))
    return parse_response(response)

def bulk_update(bulk_data_json):
    t1 = time.time()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-ndjson'
    }
    response = requests.post(URL + '/_bulk', data=bulk_data_json, headers=headers)
    print(response)
    print(response.text)
    t2 = time.time()
    print('Time took to bulk update is {0} sec'.format(t2-t1))


def insert_doc(doc_dict, index_name):
    response = requests.post(URL + index_name + '/_doc/' + doc_dict['id'],
                             data=json.dumps(doc_dict), headers=HEADERS)
    print(response)


def add_dummy_vms(index_name):
    t1 = time.time()
    for es_vm in es_const.ES_VMS:
        insert_doc(es_vm, index_name)
    t2 = time.time()
    print('Time took to insert {0} documents is {1} sec'.format(len(es_const.ES_VMS), t2-t1))


def get_vcenter_vms():
    return const.VMS

def get_vcenter_datastores():
    return const.DATASTORES

def get_es_vms():
    return es_const.ES_VMS


def persist_vms(vcenter_vms, ds_info, index_name='vms'):
    print('vcenter_vms: {0}'.format(vcenter_vms))
    es_vms = get_documents(index_name)
    print('es_vms: {0}'.format(es_vms))
    vm_ids_to_remove = [vm['_id'] for vm in es_vms]
    bulk_docs = []
    for vcenter_vm in vcenter_vms:
        # vcenter_vm = cache_vms.get('vcenter_vm')
        for es_vm in es_vms:
            if vcenter_vm['instanceUUID'] == es_vm['_source']['instanceUUID']:
                print('VM instanceUUID: {0} found. Updating existing entry'.format(vcenter_vm['instanceUUID']))
                bulk_docs.append({
                    "update": {
                        "_index": index_name,
                        "_id": es_vm['_id'],
                        "if_seq_no": es_vm['_seq_no'],
                        "if_primary_term": es_vm['_primary_term']
                    }
                })
                ds = es_vm.get('datastores')
                if ds:
                    ds.append(ds_info)
                else:
                    ds = [ds_info]
                bulk_docs.append({"doc": {'datastores': ds}})

                vm_ids_to_remove.remove(es_vm['_id'])
                break
        else:
            vm_id = str(uuid.uuid4())
            print('VM instanceUUID: {0} Not found. Adding new entry'.format(vcenter_vm['instanceUUID']))
            bulk_docs.append({"index": {"_index": index_name, "_id": vm_id}})
            bulk_docs.append({'moref': vcenter_vm['moref'], 'datastores': [ds_info]})

    print('vm_ids_to_remove: {0}'.format(vm_ids_to_remove))
    for vm_id_to_remove in vm_ids_to_remove:
        bulk_docs.append({"delete": {"_index": index_name, "_id": vm_id_to_remove}})

    if bulk_docs:
        bulks_update_json = "\n".join([json.dumps(d) for d in bulk_docs])
        bulks_update_json += "\n"
        print('bulks_update_json: {0}'.format(bulks_update_json))
        bulk_update(bulks_update_json)
    else:
        print('Everything is up to date')


def delete_index(index_name):
    response = requests.delete(URL + index_name)
    print(response)
    print(response.text)


def delete_indices(indices):
    for index in indices:
        delete_index(index)


def build_vcenter_inventory():
    vcenter_dict = {
        "id": VCENTER_ID, # doc id of vcenter host
        "name": "vcenter1",
        "hosts": [
            {
                "moref": "host-1",
                "name": "Host1",
                "datastores": [
                    {
                        "moref": "ds-1",
                        "name": "Datastore1",
                        "folder": {
                            "moref": "group-s1",
                            "name": "dsFolder1"
                        },
                        "vms": [
                            {
                                "moref": "vm-1",
                                "name": "vm1",
                                "folder":{
                                    "moref": "group-1",
                                    "name": "vmFolder1"
                                }
                            },
                            {
                                "moref": "vm-3",
                                "name": "vm3",
                                "folder": {
                                    "moref": "group-2",
                                    "name": "vmFolder2"
                                }
                            }
                        ]
                    },
                    {
                        "moref": "ds-2",
                        "name": "Datastore2",
                        "folder": {
                            "moref": "group-s1",
                            "name": "dsFolder1"
                        },
                        "vms": [
                            {
                                "moref": "vm-2",
                                "name": "vm2",
                                "folder": {
                                    "moref": "group-1",
                                    "name": "vmFolder1"
                                }
                            },
                            {
                                "moref": "vm-3",
                                "name": "vm3",
                                "folder": {
                                    "moref": "group-2",
                                    "name": "vmFolder2"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "moref": "host-2",
                "name": "Host2",
                "datastores": [
                    {
                        "moref": "ds-3",
                        "name": "Datastore3",
                        "folder": {
                            "moref": "group-s1",
                            "name": "dsFolder1"
                        },
                        "vms": [
                            {
                                "moref": "vm-4",
                                "name": "vm4",
                                "folder": {
                                    "moref": "group-1",
                                    "name": "vmFolder1"
                                }
                            }
                        ]
                    },
                    {
                        "moref": "ds-4",
                        "name": "Datastore4",
                        "folder": {
                            "moref": "group-s1",
                            "name": "dsFolder1"
                        },
                        "vms": [
                            {
                                "moref": "vm-5",
                                "name": "vm5",
                                "folder": {
                                    "moref": "group-1",
                                    "name": "vmFolder1"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return vcenter_dict


def build_bulk_docs(vcenter_dict):
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

    :param vcenter_dict:
    :return:
    """
    bulk_docs = []
    esx_index = 'poc-esxs'
    ds_index = 'poc-datastores'
    vm_index = 'poc-vms'
    folder_index = 'poc-folders'
    vm_ds_map = dict()
    folder_moref_map = dict()
    vcenter_info = {
        'id': vcenter_dict['id'],
        'name': vcenter_dict['name']
    }
    hosts = vcenter_dict.get('hosts', [])
    if not hosts:
        print('No host found.')

    for esx in hosts:
        esx_id = str(uuid.uuid4())
        esx_details = {
            'id': esx_id,
            'name': esx['name']
        }
        datastores = esx.pop('datastores', [])
        bulk_docs.append({"index": {"_index": esx_index, "_id": esx_id}})
        esx.update({'vcenterInfo': vcenter_info})
        bulk_docs.append(esx)
        for datastore in datastores:
            ds_id = str(uuid.uuid4())
            ds_info = {
                'id': ds_id,
                'name': datastore['name']
            }
            vms = datastore.pop('vms', [])
            ds_folder_info = datastore.pop('folder', None)
            if ds_folder_info:
                folder_info = folder_moref_map.get(ds_folder_info['moref'])
                if not folder_info:
                    folder_id = str(uuid.uuid4())
                    folder_info = {
                        'id': folder_id,
                        'name': ds_folder_info['name']
                    }
                    folder_moref_map[ds_folder_info['moref']] = folder_info
                    bulk_docs.append({
                        "index": {"_index": folder_index, "_id": folder_id}
                    })
                    bulk_docs.append(ds_folder_info)

            bulk_docs.append({"index": {"_index": ds_index, "_id": ds_id}})
            datastore.update({
                'esxInfo': esx_details,
                'vcenterInfo': vcenter_info,
                'folderInfo': folder_info
            })
            bulk_docs.append(datastore)
            for vm in vms:
                vm_folder_info = vm.pop('folder', None)
                if vm_folder_info:
                    folder_info = folder_moref_map.get(vm_folder_info['moref'])
                    if not folder_info:
                        folder_id = str(uuid.uuid4())
                        folder_info = {
                            'id': folder_id,
                            'name': vm_folder_info['name']
                        }
                        folder_moref_map[vm_folder_info['moref']] = folder_info
                        bulk_docs.append({
                            "index": {"_index": folder_index, "_id": folder_id}
                        })
                        bulk_docs.append(vm_folder_info)

                if vm_ds_map.get(vm['moref']):
                    print('VM moref : {0}  found, updating existing one'.format(vm['moref']))
                    # already added to persist, need to update only dsInfo
                    vm_details = vm_ds_map.get(vm['moref'])
                    vm_ds_info = vm_details['dsInfo']
                    vm_ds_info.append(ds_info)
                    bulk_docs.append({
                        "update": {
                            "_index": vm_index,
                            "_id": vm_details['id'],
                        }
                    })
                    bulk_docs.append({
                        "doc": {
                            'dsInfo': vm_ds_info
                        }
                    })
                else:
                    print('VM moref : {0} not found, adding new'.format(vm['moref']))
                    vm_id = str(uuid.uuid4())
                    vm_ds_map[vm['moref']] = {
                        'dsInfo': [ds_info],
                        'id': vm_id
                    }
                    bulk_docs.append({"index": {"_index": vm_index, "_id": vm_id}})
                    vm.update({
                        'dsInfo': [ds_info],
                        'vcenterInfo': vcenter_info,
                        'esxInfo': esx_details,
                        'folderInfo': folder_info
                    })
                    bulk_docs.append(vm)
    return bulk_docs


# def process_bulk_docs(self, doc_list):
#     # Convert data to line delimited json data.
#     formatted_data = '\n'.join(json.dumps(data) for data in doc_list)
#     formatted_data += '\n'
#     uri = constants.BULK_URI + constants.EXPLICIT_REFRESH_URI
#     es_client.es_request(uri, formatted_data, 'POST')

def persist_bulk_docs(bulk_docs):
    if bulk_docs:
        bulks_update_json = "\n".join([json.dumps(d) for d in bulk_docs])
        bulks_update_json += "\n"
        print('bulks_update_json: {0}'.format(bulks_update_json))
        bulk_update(bulks_update_json)
    else:
        print('Nothing to update')


def build_cache():
    vcenter_dict = build_vcenter_inventory()
    bulk_docs = build_bulk_docs(vcenter_dict)
    persist_bulk_docs(bulk_docs)


def get_vcentory_inventory_change():
   vcenter_change_dict = {
       "id": VCENTER_ID,  # doc id of vcenter host
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
   return vcenter_change_dict


RESOURCE_ESX = 'poc-esxs'
RESOURCE_DATASTORE = 'poc-datastores'
RESOURCE_VM = 'poc-vms'
RESOURCE_FOLDER = 'poc-folders'


class ESCacheUpdateHelper:
    def __init__(self, vcenter_change_dict):
        self.vcenter_dict = vcenter_change_dict
        self.vcenter_info = {
            'id':  self.vcenter_dict['id'],
            'name':  self.vcenter_dict['name']
        }
        self.bulk_docs = []

    def _build_esx_docs(self, esx_details):
        if esx_details:
            esx_details.pop('datastores', [])
            esx_details.update({'vcenterInfo': self.vcenter_info})
            query = create_multiple_terms_query({"moref.keyword": [esx_details['moref']]})
            es_vm_esx_details = get_by_query(RESOURCE_ESX, query)
            esx_info = {
                'name': esx_details['name']
            }
            if es_vm_esx_details:
                esx_info['id'] = es_vm_esx_details[0]['_id']
                self.bulk_docs.append({"index": {"_index": RESOURCE_ESX, "_id": es_vm_esx_details[0]['_id']}})
                self.bulk_docs.append({"doc": esx_details})
            else:
                esx_id = str(uuid.uuid4())
                esx_info['id'] = esx_id
                self.bulk_docs.append({"index": {"_index": RESOURCE_ESX, "_id": esx_id}})
                self.bulk_docs.append(esx_details)


    def build_bulk_docs(self):
        """
        Build the data in following format:

        :param vcenter_dict:
        :return:
        """
        bulk_docs = []
        esx_index = 'poc-esxs'
        ds_index = 'poc-datastores'
        vm_index = 'poc-vms'
        folder_index = 'poc-folders'
        vm_ds_map = dict()
        folder_moref_map = dict()
        vms = self.vcenter_dict.get('vms', [])
        if not vms:
            print('No vms found.')

        for vm in vms:
            action = vm['action']
            vm_details = vm['details']

            # Fetch VM's Esx details and perisist/update it
            esx_info = None
            vm_esx_details = vm_details.pop('host', None) # in case of remove, it will not be there
            self._build_esx_docs(vm_esx_details)
            if vm_esx_details:
                vm_esx_details.pop('datastores', [])
                vm_esx_details.update({'vcenterInfo': vcenter_info})
                query = create_multiple_terms_query({"moref.keyword": [vm_esx_details['moref']]})
                es_vm_esx_details = get_by_query(esx_index, query)
                esx_info = {
                    'name': vm_esx_details['name']
                }
                if es_vm_esx_details:
                    esx_info['id'] = es_vm_esx_details[0]['_id']
                    bulk_docs.append({"index": {"_index": esx_index, "_id": es_vm_esx_details[0]['_id']}})
                    bulk_docs.append({"doc": vm_esx_details})
                else:
                    esx_id = str(uuid.uuid4())
                    esx_info['id'] = esx_id
                    bulk_docs.append({"index": {"_index": esx_index, "_id": esx_id}})
                    bulk_docs.append(vm_esx_details)

            # Fetch VM Datastore details and perisist/update it
            ds_info = []
            vm_datastores = vm_details.pop('datastores', [])
            if vm_datastores:
                for datastore in vm_datastores:
                    # get datastore folder details
                    ds_folder_details = datastore.pop('folder', None)
                    ds_folder_details.update({'vcenterInfo': vcenter_info})
                    query = create_multiple_terms_query({"moref.keyword": [ds_folder_details['moref']]})
                    es_ds_folder_details = get_by_query(folder_index, query)
                    ds_folder_info = {
                        'name': ds_folder_details['name']
                    }
                    if es_ds_folder_details:
                        ds_folder_info['id'] = es_ds_folder_details[0]['_id']
                        bulk_docs.append({"index": {"_index": folder_index, "_id": es_ds_folder_details[0]['_id']}})
                        bulk_docs.append({"doc": ds_folder_details})
                    else:
                        folder_id = str(uuid.uuid4())
                        ds_folder_info['id'] = folder_id
                        bulk_docs.append({"index": {"_index": folder_index, "_id": folder_id}})
                        bulk_docs.append(ds_folder_details)
                    # get datastore details from ES
                    query = create_multiple_terms_query({"moref.keyword": [datastore['moref']]})
                    es_ds_details = get_by_query(ds_index, query)
                    if es_ds_details:
                        ds_info.append({
                            'id': es_ds_details[0]['_id'],
                            'name': es_ds_details[0]['_source']['name']
                        })
                    else:
                        ds_id = str(uuid.uuid4())
                        bulk_docs.append({"index": {"_index": ds_index, "_id": ds_id}})
                        datastore.update({'vcenterInfo': vcenter_info, 'esxInfo': esx_info,'folderInfo': ds_folder_info})
                        bulk_docs.append(datastore)
                        ds_info.append({
                            'id': ds_id,
                            'name': datastore['name']
                        })

            # Fetch VM's Folder details and perisist/update it
            vm_folder_info = None
            vm_folder_details = vm_details.pop('folder', None)
            if vm_folder_details:
                vm_folder_details.update({'vcenterInfo': vcenter_info})
                query = create_multiple_terms_query({"moref.keyword": [vm_folder_details['moref']]})
                es_vm_folder_details = get_by_query(folder_index, query)
                vm_folder_info = {
                    'name': vm_folder_details['name']
                }
                if es_vm_folder_details:
                    vm_folder_info['id'] = es_vm_folder_details[0]['_id']
                    bulk_docs.append({"index": {"_index": folder_index, "_id": es_vm_folder_details[0]['_id']}})
                    bulk_docs.append({"doc": vm_folder_details})
                else:
                    folder_id = str(uuid.uuid4())
                    vm_folder_info['id'] = folder_id
                    bulk_docs.append({"index": {"_index": folder_index, "_id": folder_id}})
                    bulk_docs.append(vm_folder_details)

            query = create_multiple_terms_query({"moref.keyword": [vm_details['moref']]})
            es_vm_details = get_by_query(vm_index, query)
            msg = 'Object: VM, Action: {0}, Found ES entry: {1}'.format(action, True if es_vm_details else False)
            print(msg)

            vm_details.update({
                'vcenterInfo': vcenter_info,
                'dsInfo': ds_info,
                'esxInfo': esx_info,
                'folderInfo': vm_folder_info
            })

            if action == 'ADD':
                if es_vm_details:
                    bulk_docs.append({"index": {"_index": vm_index, "_id": es_vm_details[0]['_id']}})
                    bulk_docs.append({"update": vm_details})
                else:
                    vm_id = str(uuid.uuid4())
                    bulk_docs.append({"index": {"_index": vm_index, "_id": vm_id}})
                    bulk_docs.append(vm_details)
            elif action == 'Remove' and es_vm_details:
                 bulk_docs.append({"delete": {"_index": vm_index, "_id": es_vm_details[0]['_id']}})
            elif action == 'Modify':
                bulk_docs.append({"index": {"_index": vm_index, "_id": es_vm_details[0]['_id']}})
                bulk_docs.append({"doc": vm_details})

        datastores = vcenter_dict.get('datastores', [])
        if not datastores:
            print('No datastore found to update.')

        for datastore in datastores:
            action = datastore['action']
            ds_details = datastore['details']

            # Fetch Datastore ESX details and persists/update it
            esx_info = None
            ds_esx_details = ds_details.pop('host', None)
            if ds_esx_details:
                query = create_multiple_terms_query({"moref.keyword": [ds_esx_details['moref']]})
                es_esx_details = get_by_query(esx_index, query)
                esx_info = {
                    'name': ds_esx_details['name']
                }
                ds_esx_details.update({'vcenterInfo': vcenter_info})
                ds_esx_details.pop('datastores', [])

                if es_esx_details:
                    esx_info['id'] = es_esx_details[0]['_id']
                    bulk_docs.append({"index": {"_index": esx_index, "_id": es_esx_details[0]['_id']}})
                    bulk_docs.append({"doc": ds_esx_details})
                else:
                    esx_id = str(uuid.uuid4())
                    esx_info['id'] = esx_id
                    bulk_docs.append({"index": {"_index": esx_index, "_id": esx_id}})
                    bulk_docs.append(ds_esx_details)

            # Fetch Datastore's folder details and persists/update it
            ds_folder_info = None
            print('datastore: {0}'.format(datastore))

            ds_folder_details = ds_details.pop('folder', None)
            print('ds_folder_details: {0}'.format(ds_folder_details))
            if ds_folder_details:
                ds_folder_details.update({'vcenterInfo': vcenter_info})
                query = create_multiple_terms_query({"moref.keyword": [ds_folder_details['moref']]})
                es_ds_folder_details = get_by_query(folder_index, query)
                print('es_ds_folder_details: {0}'.format(es_ds_folder_details))

                ds_folder_info = {
                    'name': ds_folder_details['name']
                }
                if es_ds_folder_details:
                    ds_folder_info['id'] = es_ds_folder_details[0]['_id']
                    bulk_docs.append({"index": {"_index": folder_index, "_id": es_ds_folder_details[0]['_id']}})
                    bulk_docs.append({"doc": ds_folder_details})
                else:
                    folder_id = str(uuid.uuid4())
                    ds_folder_info['id'] = folder_id
                    bulk_docs.append({"index": {"_index": folder_index, "_id": folder_id}})
                    bulk_docs.append(ds_folder_details)

            ds_details.pop('vms', None)
            print('ds_folder_info: {0}'.format(ds_folder_info))

            ds_details.update({
                'vcenterInfo': vcenter_info,
                'esxInfo': esx_info,
                'folderInfo': ds_folder_info
            })

            query = create_multiple_terms_query({"moref.keyword": [ds_details['moref']]})
            es_ds_details = get_by_query(ds_index, query)
            msg = 'Action: {0}, Found ES entry: {1}'.format(action, True if es_ds_details else False)
            print(msg)

            if action == 'ADD':
                if es_ds_details:
                    bulk_docs.append({"index": {"_index": ds_index, "_id": es_ds_details[0]['_id']}})
                    bulk_docs.append({"doc": ds_details})
                else:
                    ds_id = str(uuid.uuid4())
                    bulk_docs.append({"index": {"_index": ds_index, "_id": ds_id}})
                    bulk_docs.append(ds_details)
            elif action == 'Remove' and es_ds_details:
                bulk_docs.append({"delete": {"_index": ds_index, "_id": es_ds_details[0]['_id']}})
            elif action == 'Modify' and es_ds_details:
                bulk_docs.append({"index": {"_index": ds_index, "_id": es_ds_details[0]['_id']}})
                bulk_docs.append({"doc": ds_details})

        hosts = vcenter_dict.get('hosts', [])
        for esx in hosts:
            action = esx['action']
            esx_details = esx['details']
            esx_details.pop('datastores', None)
            esx_details.update({'vcenterInfo': vcenter_info})
            query = create_multiple_terms_query({"moref.keyword": [esx_details['moref']]})
            es_esx_details = get_by_query(esx_index, query)
            print(es_esx_details)
            msg = 'Object: Host, Action: {0}, Found ES entry: {1}'.format(action, True if es_esx_details else False)
            print(msg)
            if action == 'ADD':
                if es_esx_details:
                    bulk_docs.append({"index": {"_index": esx_index, "_id": es_esx_details[0]['_id']}})
                    bulk_docs.append({"doc": esx_details})
                else:
                    esx_id = str(uuid.uuid4())
                    bulk_docs.append({"index": {"_index": esx_index, "_id": esx_id}})
                    bulk_docs.append(esx_details)
            elif action == 'Remove' and es_esx_details:
                bulk_docs.append({"delete": {"_index": esx_index, "_id": es_esx_details[0]['_id']}})
            elif action == 'Modify' and es_esx_details:
                bulk_docs.append({"index": {"_index": esx_index, "_id": es_esx_details[0]['_id']}})
                bulk_docs.append({"doc": esx_details})
        return bulk_docs

# Note:
# event should be sorted by time(older  events should come first)

def update_cache():
    vcenter_changed_dict = get_vcentory_inventory_change()
    changed_bulk_docs = build_cache_update_bulk_docs(vcenter_changed_dict)
    persist_bulk_docs(changed_bulk_docs)


def create_multiple_terms_query(params):
    query = {
        "query": {
            "bool": {
                "must": []
            }
        }
    }
    for k, v in params.items():
        query['query']['bool']['must'].append({
            'terms': {k: v}
        })
    return query



if __name__ == '__main__':
    #build_cache()
    update_cache()
    #delete_indices(['poc-vms', 'poc-datastores', 'poc-esxs', 'poc-folders']) # only clean up



    # query1 = {
    #     "query": {
    #         "match": {
    #             "moref": "ds-1",
    #             "vcenterInfo.id": "e9bb42b4-8210-4555-889f-485eed44bc9d"
    #         }
    #     }
    # }
    query2 = {
      "query": {
        "bool": {
          "must": [
            {"terms": {"moref.keyword": ["ds-1"]}},
            {"terms": {"vcenterInfo.id.keyword": ["e9bb42b4-8210-4555-889f-485eed44bc9d"]}}

          ]
        }
      }
    }
    query3 = {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"moref.keyword": ["host-1"]}},

                ]
            }
        }
    }
    #print(get_by_query('poc-esxs', create_multiple_terms_query({"moref.keyword": ["host-3"]})))

    query3 = {
      "query": {
        "bool": {
          "must": [
            {
              "match": {
                "moref": "ds-1"
              }
            },
            {
              "match": {
                "vcenterInfo.id": "e9bb42b4-8210-4555-889f-485eed44bc9d-1"
              }
            }
          ]
        }
      }
    }
    #print(get_by_query('poc-datastores', query2))

    # index_name = 'cache-vms'
    # add_dummy_vms(index_name) # One time
    # get_documents(index_name)
    # for i in range(5):
    #     if i == 4:
    #         print('found')
    #         break
    # else:
    #     print("Not found") # If loop traverse completed
