import requests
import json

URL = 'http://localhost:9200/'


def parse_response(search_response):
    if search_response.status_code == 200:
        documents = search_response.json()['hits']['hits']
        print(documents)
        docs = []
        for document in documents:
            doc = {
                'id': document['_id']
            }
            doc.update(document['_source'])
            docs.append(doc)
        return docs


def get_documents(index_name):
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(URL + index_name + "/_search", headers=headers)
    print(response)
    print(parse_response(response))


def bulk_update(doc_list, index_name):
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


def add_users():
    users = [
        {
            'id': 1,
            'name': 'Aafak'
        },
        {
            'id': 2,
            'name': 'Ajay'
        },
        {
            'id': 3,
            'name': 'Aman'
        },
        {
            'id': 4,
            'name': 'Aakash'
        }
    ]
    bulk_update(users, 'users')


if __name__ == '__main__':
    # get_documents('employee2')
    # add_users()
    get_documents('users')
