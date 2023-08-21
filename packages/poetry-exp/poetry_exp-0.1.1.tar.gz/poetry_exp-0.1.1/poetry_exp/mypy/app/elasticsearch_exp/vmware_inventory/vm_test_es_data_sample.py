# (C) Copyright 2020 Hewlett Packard Enterprise Development Company, L.P.
import sys
import uuid

import json
import unittest

from datetime import datetime
from app_catalog.es_data.common.es_client import es_request

sys.path.append(".")
from app_catalog.es_data.core import manager as mgr  # noqa
from app_catalog.es_data.transformer.core import generic as gt  # noqa


class TestES(unittest.TestCase):
    '''
    This is only a sample Test Class to have a
    quick way if needed to check if any api change
    is broken.
    or for any future test case addition as bandwidth
    allows :)

    '''

    def setUp(self):
        self.es_manager = mgr.ESDataManager()

    def test_0_setup(self):
        # Clean up all indices from ES.
        es_request('/*', data=None, method='DELETE')
        self.es_manager.setup()
        self._log(self._testMethodName, b"Setup Completed", 0)

    def _log(self, testMethodName, body, status):
        print('{:>1s} {:>1s} {:>1s} {:>1d}'.format(
            '\n' + testMethodName, ":", body.decode(), status))

    def _execute_crud_operations(self, sample_data, resource):
        t_uuid = str(uuid.uuid4())
        now = datetime.now()
        print("Start =", now)
        sample_data['id'] = t_uuid
        body, status = self.es_manager.process(
            'PUT', resource,
            doc_id=t_uuid, data=sample_data)
        self._log(self._testMethodName + ': PUT', body, status)
        print("PUT Complete =", now)

        body, status = self.es_manager.process(
            'GET', resource, doc_id=t_uuid)
        self._log(self._testMethodName + ': GET_BY_ID', body, status)
        print("GET Complete =", now)

        sample_query_all = \
            {"query": {"match_all": {}}, "from": 0, "size": 100}
        body, status = self.es_manager.process(
            'GET', resource, query=sample_query_all)
        self._log(self._testMethodName + ': GET_ALL', body, status)
        print("GET ALL Complete =", now)

        # body, status = self.es_manager.process(
        #     'DELETE', resource, doc_id=t_uuid)
        # self._log(self._testMethodName + ': DELETE_BY_ID', body, status)
        print("DELETE Complete =", now)

    def test_ss_generic_transform(self):
        """
         This is for testing the generic transform()
        """
        sample_source_data_dict = \
            {
                'ip_address': '127.0.0.1',
                'ip_address_extra': {'level2': 'level2value'},
                'name': 'test',
                'description': 'this is a test description',
                'name_alias': 'test_alias',
                'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                'status': 'available',
                'state': 'available',
                'state_reason': 'some reason',
                'created_at': '2020-01-27T04:04:34Z',
                'updated_at': '2020-01-27T04:04:34Z',
                'credential_id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e10',
                'device_type': 'SQL',
                'native_data_mover_enabled': True,
                'storage_system_metadata': ['this', 'is', 'a', 'metadata'],
                'tags': [{
                    'tag_id': 'thisisatagid-',
                    'tag_name': 'finance'
                }, {
                    'tag_id': 'thisisatagid-1',
                    'tag_name': 'finance-1'
                }],
                'serial_number': 'HF54MHJ876Z',
                'device_model': 'model',
                'firmware_version': '2.3.4',
                'licenses': ['this', 'is', 'a', 'license'],
                'fc': ['this', 'is', 'a', 'fc', 'record'],
                'iscsi': [{
                    'status': 'ready',
                    'managed': True,
                    'vlan': True,
                    'network_address': '172.17.2.18',
                    'mtu': 1500,
                    'rate': 10,
                    'nsp': '0:2:1'
                }, {
                    'status': 'ready',
                    'managed': True,
                    'vlan': True,
                    'network_address': '172.17.2.82',
                    'mtu': 1500,
                    'rate': 10,
                    'nsp': '0:2:2'
                }]

            }

        test_data = gt.GenericTransformer()
        test_data.transform(sample_source_data_dict, 'test_spec')
        print(json.dumps(test_data.data, indent=2))

    def test_CRUD_vms(self):
        """
         This is for testing CRUD operations on snapshots.
        """
        sample_data = \
            {
                'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                'name': 'vm1',
                'moref': 'vm-1',
                'status': 'OK',
                'state': 'available',
                'stateReason': 'available',
                'createdAt': '2020-08-05T04:04:34Z',
                'updatedAt': '2020-08-05T04:04:34Z',
                'tags': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'Dev'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'QA'
                }],
                'networkAddress': '172.17.29.165',
                'uid': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a1',
                'appType': 'VMware',
                'protection': 'Full',
                'powerState': 'On',
                'policyJobInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a2'
                },
                'policyInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a3',
                    'name': 'Gold',
                    'type': 'AppliancePredefined'
                },
                'assetGroupsInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a4',
                    'name': 'asset-group1'
                },
                'volumeSetInfo': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a5',
                    'name': 'vol-set-name1',
                    'label': 'vol-set-label1'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a6',
                    'name': 'vol-set-name2',
                    'label': 'vol-set-label2'
                }],
                'metadata': {
                    'cbtEnabled': True
                },
                'projects': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a7',
                    'name': 'Test & Dev'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a8',
                    'name': 'Production'
                }],
                'tools': {
                    'version': '3.0',
                    'type': 'GuestTool'
                },
                'computeInfo': {
                    'numCPUCores': 4,
                    'numCPUThreads': 2,
                    'memorySizeInMiB': '1024MB'
                },
                'platformInfo': {
                    'type': 'Windows',
                    'name': 'SQL Server',
                    'releaseVersion': '16.0',
                    'buildVersion': '3009'
                },
                'clone': True,
                'cloneInfo': {
                    'sourceVMInfo': {
                        'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a9',
                        'name': 'vm2'
                    },
                    'parentVMInfo': {
                        'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a8',
                        'name': 'vm5'
                    }
                },
                'createdByInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73b1',
                    'name': 'admin'
                },
                'diskUuidEnabled': True,
                'vmxConfigPath': 'vm1.vmx',
                'snapshots': {
                    'hasSnapshots': True
                },
                "vcenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                },
                "clusterInfo": {
                    'moref': "domain-c1",
                    'name': 'Cluster1'
                },
                "datacenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                },
                "esxInfo": {
                    "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e3",
                    "name": "Host1"
                },
                "datastoreInfo": [
                    {
                        "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e4",
                        "name": "Datastore1"
                    },
                    {
                        "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e5",
                        "name": "Datastore2"
                    },
                ]

            }
        self._execute_crud_operations(sample_data, 'vms')

    def test_CRUD_datastores(self):
        """
         This is for testing CRUD operations on snapshots.
        """
        sample_data = \
            {
                'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                'name': 'ds1',
                'moref': 'datastore-1',
                'status': 'Ok',
                'state': 'available',
                'stateReason': 'available',
                'createdAt': '2020-08-05T04:04:34Z',
                'updatedAt': '2020-08-05T04:04:34Z',
                'tags': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'Dev'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'QA'
                }],
                'uid': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a1',
                'appType': 'VMware',
                'type': 'VMFS',
                'protection': 'Full',
                'policyJobInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a2'
                },
                'policyInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a3',
                    'name': 'Gold',
                    'type': 'AppliancePredefined'
                },
                'assetGroupsInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a4',
                    'name': 'asset-group1'
                },
                'volumeSetInfo': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a5',
                    'name': 'vol-set-name1',
                    'label': 'vol-set-label1'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a6',
                    'name': 'vol-set-name2',
                    'label': 'vol-set-label2'
                }],
                'metadata': {
                    'type': 'vmfs'
                },
                'projects': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a7',
                    'name': 'Test & Dev'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73a8',
                    'name': 'Production'
                }],
                'createdByInfo': {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73b1',
                    'name': 'admin'
                },
                "vcenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                },
                "clusterInfo": {
                    'moref': "domain-c1",
                    'name': 'Cluster1'
                },
                "datacenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                },
                "esxInfo": [
                    {
                        "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e7",
                        "name": "Host1"
                    },
                    {
                        "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e8",
                        "name": "Host2"
                    },
                ]

            }
        self._execute_crud_operations(sample_data, 'datastores')

    def test_CRUD_esxs(self):
        """
         This is for testing CRUD operations on snapshots.
        """
        sample_data = \
            {
                'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                'name': 'Host1',
                'moref': 'host-1',
                'status': 'available',
                'state': 'available',
                'createdAt': '2020-08-05T04:04:34Z',
                'updatedAt': '2020-08-05T04:04:34Z',
                'tags': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'Dev'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'QA'
                }],
                "vcenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                },
                "clusterInfo": {
                    'moref': "domain-c1",
                    'name': 'Cluster1'
                },
                "datacenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                }

            }
        self._execute_crud_operations(sample_data, 'esxs')

    def test_CRUD_folders(self):
        """
         This is for testing CRUD operations on snapshots.
        """
        sample_data = \
            {
                'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                'name': 'vmFolder1',
                'moref': 'group-1',
                'status': 'available',
                'state': 'available',
                'createdAt': '2020-08-05T04:04:34Z',
                'updatedAt': '2020-08-05T04:04:34Z',
                'tags': [{
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'Dev'
                }, {
                    'id': '19d11ef7-cfc4-4fd8-9dc1-1bb0700e73e9',
                    'name': 'QA'
                }],
                "type": "vm",
                "parentInfo": {
                    "moref": "group-0",
                    "name": "vm"
                },
                "subFolders": [
                    {
                        "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e736",
                        "name": "sunFolder1(vmFolder1)"
                    },
                    {
                        "id": "19d11ef7-cfc4-4fd8-9dc1-1bb0700e736",
                        "name": "sunFolder1(vmFolder1)"
                    },
                ],
                "vcenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                },
                "clusterInfo": {
                    'moref': "domain-c1",
                    'name': 'Cluster1'
                },
                "datacenterInfo": {
                    "moref": "datacenter-1",
                    "name": "Datacenter1"
                }

            }
        self._execute_crud_operations(sample_data, 'folders')

    def tearDown(self):
        '''
        Placeholder for now.
        '''
        pass


if __name__ == '__main__':
    unittest.main()
