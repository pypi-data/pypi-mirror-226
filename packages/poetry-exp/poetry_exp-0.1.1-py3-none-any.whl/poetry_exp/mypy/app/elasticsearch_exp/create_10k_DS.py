import requests
import json
import time

URL = 'http://localhost:9200/'


def parse_response(search_response):
    if search_response.status_code == 200:
        documents = search_response.json()['hits']['hits']
        #return [doc['_source'] for doc in documents]
        return documents


def get_documents(index_name):
    headers = {
        'accept': 'application/json'
    }
    # /_search?filter_path=hits.hits._source
    response = requests.get(
        URL + index_name + "/_search?size=10000&seq_no_primary_term=true", headers=headers)
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
    t1 = time.time()
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
    #print(bulk_data_json)
    response = requests.post(URL + '/_bulk', data=bulk_data_json, headers=headers)
    print(response)
    #print(response.text)
    t2 = time.time()
    print('Time took to insert {0} documents is {1} sec'.format(len(bulk_docs), t2-t1))


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
    t1 = time.time()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-ndjson'
    }
    bulk_docs = []
    for document in doc_list:
        index_details = {
            "update": {
                "_index": index_name,
                "_id": document.pop('_id'),
                #"retry_on_conflict": 3,
                "if_seq_no": document.pop('_seq_no'),
                "if_primary_term": document.pop('_primary_term')
                # "version": 1 # "Update requests do not support versioning. Please use `if_seq_no` and `if_primary_term` instead"

            }

        }
        bulk_docs.append(index_details)
        bulk_docs.append({"doc": document['_source']})

    bulk_data_json = "\n".join([json.dumps(d) for d in bulk_docs])
    bulk_data_json += "\n"
    #print(bulk_data_json)
    response = requests.post(URL + '/_bulk', data=bulk_data_json, headers=headers)
    #print(response)
    #print(response.text)
    t2 = time.time()
    print('Time took to update {0} documents is {1} sec'.format(len(bulk_docs), t2-t1))


def add_ds(count=10000):
    datastores = []
    for i in range(1, count):
        datastores.append({
            "id": i,
            "name": "Datastore" + str(i),
            "protectionGroup": "protectionGroup" + str(i)
        })

    bulk_insert(datastores, 'datastores')


def update_ds():
    # Fetch VMs from vcenter
    # Traverse through the VMs fetch from vcenter
    # check if VM exist in ES, if not exists create entry for it, otherwise update it
    # Remove the existing VMs from ES if removed from vcenter
    t1 = time.time()
    datastores = get_documents('datastores')
    for datastore in datastores:
        # print(datastore)
        # doc = get_document_by_id('datastores', datastore['id'])
        # datastore['_seq_no'] = doc['_seq_no']
        # datastore['_primary_term'] = doc['_primary_term']
        datastore['_source']['protectionGroup'] = datastore['_source']['protectionGroup'] + '_3'
    t2 = time.time()
    print('Time took to fetch {0} documents details is {1} sec'.format(len(datastores), t2-t1))

    bulk_update(datastores, 'datastores')


if __name__ == '__main__':

    # add_vms() # if index not found, it will create it
    # get_documents('virtual-machines')
    add_ds()
    # Time took to insert 19998 documents is 4.359068393707275 sec
    update_ds()
    # Time took to update 19998 documents is 2.0369155406951904 sec
    # Time took to fetch 9999 documents details is 120.93461489677429 sec



