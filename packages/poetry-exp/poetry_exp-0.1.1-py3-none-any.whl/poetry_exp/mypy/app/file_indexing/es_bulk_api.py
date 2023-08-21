import time
import json
import requests


class ESBulkApiHelper():
    """
    Helper class for using elastic search bulk API
    It first build the batch of documents for add/update/delete
    and then add/update/delete all documents in one call.
    Build the doc in the following format:
    [{'resource': 'resource_name', 'id': 'doc_id', 'operation': 'delete'}
     {'resource': 'resource_name', 'id': 'doc_id', 'operation': 'index',
      'doc': {'field1': 'value1'}},
     {'resource': 'resource_name', 'id': 'doc_id', 'operation': 'update',
      'doc': {'field1': 'value1'}, 'args': {'retry_on_conflict': 3}}]
    """
    def __init__(self):
        self._bulk_docs = []
        self._doc_id_detail_map = dict()

    def add_document(self, resource_name, doc_id, doc, add_common_attr=True):
        """
        Add new document to the given resource
        :param resource_name: Name of the resource
        :param doc_id: Uuid of the document
        :param doc: Dict containing document details
        :param add_common_attr: Weather to add common attribute or not
        common attribute(createdAt, updatedAt, state, status, stateReason)
        :return: None
        """

        self._bulk_docs.append({
            'resource': resource_name,
            'id': doc_id,
            'operation': 'index',
            'doc': doc
        })
        self._doc_id_detail_map[doc_id] = {
            'resource': resource_name,
            'id': doc_id,
            'operation': 'index',
            'doc': doc
        }

    def update_document(self, resource_name, doc_id,
                        properties_to_update, retry=True):

        """
        Update the document with given properties
        :param resource_name: Resource name
        :param doc_id: Existing document id
        :param properties_to_update: Dict containing properties
         only to be updated
        :param retry: Whether to retry or not on conflict
        :return: None
        """
        args = None
        if retry:
            args = {
                es_const.RETRY_ON_CONFLICT:
                    es_const.RETRY_ATTEMPT_ON_CONFLICT
            }
        # update the doc time
        properties_to_update[es_const.UPDATED_AT] =\
            es_utils.get_es_formatted_date_time()

        self._bulk_docs.append({
            'resource': resource_name,
            'id': doc_id,
            'operation': 'update',
            'doc': properties_to_update,
            'args': args
        })
        self._doc_id_detail_map[doc_id] = {
            'resource': resource_name,
            'id': doc_id,
            'operation': 'update',
            'doc': properties_to_update,
        }

    def delete_document(self, resource_name, doc_id):
        """
        Delete the document for given id
        :param resource_name: Name of the resource
        :param doc_id: Document id
        :return: None
        """
        self._bulk_docs.append({
            'resource': resource_name,
            'id': doc_id,
            'operation': 'delete'
        })
        self._doc_id_detail_map[doc_id] = {
            'resource': resource_name,
            'id': doc_id,
            'operation': 'delete'
        }

    def bulk_update(self):
        """
        Add/Update/Delete the bulk documents in elastic search
        :return: List of dict containing the result of each document update
        """
        update_result = {
            'status': True
        }
        if self._bulk_docs:
            print('Processing bulk documents...')
            t1 = time.time()
            bulk_update_response = self.process_bulk_update(self._bulk_docs)
            t2 = time.time()
            print('Time took to process #{0} documents is {0} seconds'
                     ''.format(len(self._bulk_docs), t2 - t1))

            # Check for errors
            errors = []
            if bulk_update_response['errors']:
                update_result['status'] = False
                print('Found errors in bulk update,'
                          ' following operations failed:')
                for item in bulk_update_response['items']:
                    for operation, details in item.items():
                        if details['status'] not in [200, 201]:
                            doc_id = details['_id']
                            doc_details = self._doc_id_detail_map.get(doc_id)
                            errors.append({
                                'errorInfo': details,
                                'docDetails': doc_details
                            })
                update_result['errors'] = errors
                print('Errors: {0}'.format(errors))
            else:
                update_result['result'] = bulk_update_response

            return update_result
        else:
            print('No documents to process')

    def process_bulk_update(self, bulk_data):
        """
        :param bulk_data: List of dict in following format
         [{'resource': 'index_name', 'id': 'doc_id', 'operation': 'delete'}
         {'resource': 'index_name', 'id': 'cea21015', 'operation': 'index',
          'doc': {'field1': 'value1'}},
         {'resource': 'index_name', 'id': '04f58f44', 'operation': 'update',
          'doc': {'field1': 'value1'}, 'args': {'retry_on_conflict': 3}}]

         It needs to be transformed to:
            [{ "index" : { "_index" : "test1", "_id" : "1" } },
             { "field1" : "value1" },
             { "update" : { "_index" : "test2", "_id" : "2" } },
             {"doc": { "field2" : "value2" }},
             { "delete" : { "_index" : "test3", "_id" : "3" } }
             ]
        :return:
        """

        formatted_data = list()

        for item in bulk_data:
            resource_name = item['resource']
            doc_id = item['id']
            operation = item['operation']
            args = item.get('args', {})
            doc = item.get('doc', None)
            non_delete_operations = ['index', 'update']
            if doc is None and operation in non_delete_operations:
                raise Exception('Invalid operation provided')

            alias = resource_name
            index_details = {
                operation: {
                    "_index": alias,
                    "_id": doc_id
                }
            }
            if args:
                index_details[operation].update(args)

            formatted_data.append(index_details)
            if operation in non_delete_operations:
                # apply the transformation
                # doc = es_utils.get_transformed_data(
                #     '/' + alias, doc)
                if operation == 'update':
                    doc = {"doc": doc}

                formatted_data.append(doc)

        # Convert data to line delimited json data.
        formatted_data = '\n'.join(json.dumps(d) for d in formatted_data)
        formatted_data += '\n'

        # uri = constants.BULK_URI + constants.EXPLICIT_REFRESH_URI
        url = 'http://localhost:9200/'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-ndjson'
        }
        #body, status = es_client.es_request(uri, formatted_data, 'POST')
        response = requests.post(url + '/_bulk', data=formatted_data, headers=headers)

        if response.status_code == 200:
            bulk_update_result = response.json()
            if bulk_update_result['errors']:
                print('Bulk update failed, result: {0}'.format(
                    bulk_update_result))
            else:
                print('Bulk updates successful.')
            return bulk_update_result
        else:
            raise Exception("Bulk Update failed")
