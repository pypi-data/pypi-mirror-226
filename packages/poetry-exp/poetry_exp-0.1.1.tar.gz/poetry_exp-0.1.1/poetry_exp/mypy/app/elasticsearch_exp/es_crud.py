import requests
import json
import time
URL = "http://localhost:9200/"
HEADERS = {
    'accept': 'application/json',
    "Content-Type": "application/json"
}


def get_all_documents(index_name):
    response = requests.get(
        URL + index_name + "/_search?size=10000&seq_no_primary_term=true", headers=HEADERS)
    print(response) # by default gives only 10 records
    print(response.json())
    #return parse_response(response)


def get_document_by_id(index_name, doc_id):
    response = requests.get(
        URL + index_name + "/_doc/" + str(doc_id), headers=HEADERS)
    print(response)
    print(response.json())
    return response.json()


def insert_doc(doc_dict, index_name):
    response = requests.post(URL + index_name + '/_doc/' + doc_dict['id'],
                             data=json.dumps(doc_dict), headers=HEADERS)
    #print(response)
    #print(response.text)


def delete_index(index_name):
    response = requests.delete(URL + index_name)
    print(response)
    print(response.text)


def add_dummy_docs(no_of_docs, index_name):
    t1 = time.time()
    for i in range(1, no_of_docs + 1):
        doc = {
            "id": str(i),
            "name":  index_name + '-' + str(i),
            "description": index_name + str(i) + '-description'
        }
        insert_doc(doc, index_name)
    t2 = time.time()
    print('Time took to insert {0} documents is {1} sec'.format(no_of_docs, t2-t1))


def update_document(doc_dict, index_name, seq_no=None, primary_term=None):
    url = URL + index_name + '/_update/' + doc_dict['doc']['id']
    if seq_no and primary_term:
        url += "?if_seq_no=" + str(seq_no) + "&if_primary_term=" + str(primary_term)
    print(url)
    response = requests.post(
        url,
        data=json.dumps(doc_dict), headers=HEADERS
    )
    print(response)
    print(response.text)


# https://www.elastic.co/guide/en/elasticsearch/guide/current/partial-updates.html
# https://discuss.elastic.co/t/update-a-same-document-on-a-same-time/39417/4
# https://discuss.elastic.co/t/handling-updates-from-multiple-sources/17309
# Partial Updates to Documents will have three step , retrieve - delete - reindex
def update_document_partially(doc_id, dict_attr_to_update, index_name, seq_no=None, primary_term=None, conflict_retries=None):
    url = URL + index_name + '/_update/' + doc_id
    if seq_no and primary_term:
        url += "?if_seq_no=" + str(seq_no) + "&if_primary_term=" + str(primary_term)
    if conflict_retries:
        url += "?retry_on_conflict=" + str(conflict_retries)
    print(url)
    response = requests.post(
        url,
        data=json.dumps({"doc": dict_attr_to_update}), headers=HEADERS
    )
    print(response)
    print(response.text)

def delete_document(doc_id, index_name):
    response = requests.delete(URL + index_name + '/_doc/' + doc_id)
    print(response)
    print(response.text)


def bulk_update(doc_list, index_name, conflict_retries=3):
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
                "retry_on_conflict": conflict_retries
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


def update_dummy_docs(no_of_docs, index_name):
    t1 = time.time()
    for i in range(1, no_of_docs + 1):
        doc = {
            "doc": {
                "id": str(i),
                "name": index_name + '-' + str(i),
                "description": index_name + str(i) + '-description-updated'
            }
        }
        update_document(doc, index_name)
    t2 = time.time()
    print('Time took to update {0} documents is {1} sec'.format(no_of_docs, t2-t1))


if __name__ == '__main__':
    #add_dummy_docs(10000, 'vms')
    #delete_index('vms')
    #get_all_documents('vms')
    #update_dummy_docs(10000, 'vms')
    #insert_doc({"id": "12345", "name": "vm_test_doc"}, 'vms')
    #get_document_by_id("vms", "12345")
    #update_document({"doc": {"id": "12345", "name": "vm_test_doc_updated"}}, 'vms')
    #get_document_by_id("vms", "12345")
    #insert_doc({"id": "12345", "name": "ds_test_doc"}, 'datastores')
    #update_document({"doc": {"id": "12345", "name": "ds_test_doc_updated"}}, 'datastores')
    #get_document_by_id("datastores", "12345")
    update_document({"doc": {"id": "12345", "name": "vm_test_doc_updated2"}}, 'vms', 20004, 1)
    get_document_by_id("vms", "12345")

    #delete_document("12345", "vms")
    #get_document_by_id("vms", "12345")


