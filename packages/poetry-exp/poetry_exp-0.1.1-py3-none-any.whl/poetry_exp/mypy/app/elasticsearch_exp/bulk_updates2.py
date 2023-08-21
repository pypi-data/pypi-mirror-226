import requests
import json

URL = 'http://localhost:9200/'


def parse_response(search_response):
    if search_response.status_code == 200:
        documents = search_response.json()['hits']['hits']
        return [doc['_source'] for doc in documents]


def get_documents(index_name):
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(
        URL + index_name + "/_search?filter_path=hits.hits._source", headers=headers)
    print(response)
    print(parse_response(response))

def get_document_by_id(index_name, doc_id):
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(
        URL + index_name + "/_doc/"+ str(doc_id), headers=headers)
    print(response)
    #print(parse_response(response))
    return response.json()

def bulk_insert(doc_list, index_name):
    """
    Build the data in following format
    {"index": {"_index": "users", "_id": 1}}
    {"id": 1, "name": "Aafak"}
    {"index": {"_index": "users", "_id": 2}}
    {"id": 2, "name": "Ajay"}
    {"index": {"_index": "users", "_id": 3}}
    {"id": 3, "name": "Aman"}
    {"index": {"_index": "users", "_id": 4}}
    {"id": 4, "name": "Aakash"}

    :param doc_list:
    :param index_name:
    :return:
    """
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-ndjson'
    }
    bulk_docs = []
    for document in doc_list:
        index_details = {
            "index": {
                "_index": index_name,
                "_id": document['id']
            }
        }
        bulk_docs.append(index_details)
        bulk_docs.append(document)

    bulk_data_json = "\n".join([json.dumps(d) for d in bulk_docs])
    bulk_data_json += "\n"
    print(bulk_data_json)
    response = requests.post(URL + '/_bulk', data=bulk_data_json, headers=headers)
    print(response)
    print(response.text)


def bulk_update(doc_list, index_name):
    """
    Build the data in following format
    {"update": {"_index": "users", "_id": 1}}
    {"id": 1, "name": "Aafak"}
    {"update": {"_index": "users", "_id": 2}}
    {"id": 2, "name": "Ajay"}
    {"update": {"_index": "users", "_id": 3}}
    {"id": 3, "name": "Aman"}
    {"update": {"_index": "users", "_id": 4}}
    {"id": 4, "name": "Aakash"}

    :param doc_list:
    :param index_name:
    :return:
    """
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-ndjson'
    }
    bulk_docs = []
    for document in doc_list:
        index_details = {
            "update": {
                "_index": index_name,
                "_id": document.pop('id'),
                #"retry_on_conflict": 3,
                "if_seq_no": document.pop('_seq_no'),
                "if_primary_term": document.pop('_primary_term')
                # "version": 1 # "Update requests do not support versioning. Please use `if_seq_no` and `if_primary_term` instead"

            }

        }
        bulk_docs.append(index_details)
        bulk_docs.append({"doc": document})

    bulk_data_json = "\n".join([json.dumps(d) for d in bulk_docs])
    bulk_data_json += "\n"
    print(bulk_data_json)
    response = requests.post(URL + '/_bulk', data=bulk_data_json, headers=headers)
    print(response)
    print(response.text)


def add_vms():
    vms = [
        {
            'id': 1,
            'name': 'vm1',
            'policy': None
        },
        {
            'id': 2,
            'name': 'vm2',
            'policy': None
        },
        {
            'id': 3,
            'name': 'vm3',
            'policy': None
        },
        {
            'id': 4,
            'name': 'vm4',
            'policy': None
        }
    ]
    bulk_insert(vms, 'virtual-machines')


def update_vms():
    # Fetch VMs from vcenter
    # Traverse through the VMs fetch from vcenter
    # check if VM exist in ES, if not exists create entry for it, otherwise update it
    # Remove the existing VMs from ES if removed from vcenter
    vms = [
        {
            'id': 1,
            'name': 'vm01',
            'policy': 'p12222',

        },
        {
            'id': 2,
            'name': 'vm02',
            'policy': 'p2'
        },
        {
            'id': 3,
            'name': 'vm03',
            'policy': 'p3'
        },
        {
            'id': 4,
            'name': 'vm04',
            'policy': 'p4'
        }
    ]
    for vm in vms:
        doc = get_document_by_id('virtual-machines', vm['id'])
        vm['_seq_no'] = doc['_seq_no']
        vm['_primary_term'] = doc['_primary_term']
    bulk_update(vms, 'virtual-machines')


if __name__ == '__main__':

    # add_vms() # if index not found, it will create it
    # get_documents('virtual-machines')
    update_vms()
    get_documents('virtual-machines')



