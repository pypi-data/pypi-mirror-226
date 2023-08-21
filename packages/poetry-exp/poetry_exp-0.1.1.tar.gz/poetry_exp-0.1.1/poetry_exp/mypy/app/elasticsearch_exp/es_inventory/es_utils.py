import json
import time
import requests
from elasticsearch_exp.es_inventory import constants
from elasticsearch_exp.es_inventory import es_const

import uuid


def generate_new_doc_id():
    return str(uuid.uuid4())


def parse_response(search_response):
    if search_response.status_code == 200:
        documents = search_response.json()['hits']['hits']
        return documents


def build_index_details(index_name, doc_id, op_type, retry=False,
                        retry_attempt=es_const.RETRY_ATTEMPT_ON_CONFLICT):

    index_details = {
        op_type: {
            es_const._INDEX: index_name,
            es_const._ID: doc_id
        }
    }
    if retry:
        index_details[op_type][es_const.RETRY_ON_CONFLICT] =\
            retry_attempt
    print(index_details)
    return index_details


def get_documents(index_name):
    headers = {
        'accept': 'application/json'
    }
    url = constants.URL + index_name + \
          "/_search?size=10000&seq_no_primary_term=true"
    print(url)
    response = requests.get(
        url, headers=headers)
    print(response)  # by default gives only 10 records
    print(response.json())
    return parse_response(response)


def get_document_by_id(index_name, doc_id):
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(
        constants.URL + index_name + "/_doc/" + str(doc_id), headers=headers)
    # print(response)
    # print(parse_response(response))
    return response.json()


def get_by_query(index_name, query):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    print(query)
    response = requests.get(
        constants.URL + index_name +
        "/_search?filter_path=hits.hits",
        data=json.dumps(query), headers=headers)
    print(response)
    # print(parse_response(response))
    return parse_response(response)


def bulk_update(bulk_data_json):
    t1 = time.time()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-ndjson'
    }
    response = requests.post(
        constants.URL + '/_bulk', data=bulk_data_json, headers=headers)
    print(response)
    print(response.text)
    t2 = time.time()
    print('Time took to bulk update is {0} sec'.format(t2-t1))


def insert_doc(doc_dict, index_name):
    response = requests.post(
        constants.URL + index_name + '/_doc/' + doc_dict['id'],
        data=json.dumps(doc_dict), headers=constants.HEADERS)
    print(response)


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


def delete_index(index_name):
    response = requests.delete(constants.URL + index_name)
    print(response)
    print(response.text)


def delete_indices(indices):
    for index in indices:
        delete_index(index)


def get_bulk_docs_json_string(bulk_docs):
    if bulk_docs:
        bulk_docs_json_string = "\n".join([json.dumps(d) for d in bulk_docs])
        bulk_docs_json_string += "\n"
        # print('bulk_docs_json_string: {0}'.format(bulk_docs_json_string))
        return bulk_docs_json_string
    else:
        print('No docs available')


def update_bulk_docs(bulk_docs):
    bulk_docs_json_string = get_bulk_docs_json_string(bulk_docs)
    t1 = time.time()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-ndjson'
    }
    response = requests.post(
        constants.URL + '/_bulk', data=bulk_docs_json_string, headers=headers)
    # print(response)
    # print(response.text)
    t2 = time.time()
    print('Time took to ES bulk update is {0} sec'.format(t2 - t1))
