BUILD_SAMPLE = {
  'id': 'f4c45eb3-de82-4c0b-9154-cad7c7702ec9',
  'name': 'VMware vCenter Server',
  'version': '6.7.0',
  'datacenters': [
    {
      'name': 'DC1',
      'moref': 'datacenter-2',
      'hosts': [
        {
          'name': '172.17.10.88',
          'moref': 'host-657',
          'parent': {
            'moref': 'domain-c741',
            'type': 'cluster'
          }
        },
        {
          'name': '172.17.10.86',
          'moref': 'host-9'
        }
      ],
      'datastores': [
        {
          'name': 'rcgroup_ds1',
          'moref': 'datastore-661',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'San_28AUG_DS',
          'moref': 'datastore-669',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'RMCDEPLOY2',
          'moref': 'datastore-674',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'rcgroup_ds2',
          'moref': 'datastore-662',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'santosh_rmcv_rcg_ds',
          'moref': 'datastore-664',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': '27_JAN_DS',
          'moref': 'datastore-679',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_8',
          'moref': 'datastore-288',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_10',
          'moref': 'datastore-290',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_2',
          'moref': 'datastore-282',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s743',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_6',
          'moref': 'datastore-286',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_1',
          'moref': 'datastore-12',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'datastore1 (2)',
          'moref': 'datastore-10',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_RMC_OVF',
          'moref': 'datastore-11',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_No_VMs',
          'moref': 'datastore-16',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'Demo_DS',
          'moref': 'datastore-186',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_7',
          'moref': 'datastore-287',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': '13_DS2',
          'moref': 'datastore-672',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'snap-1b01e8f7-12_DS2',
          'moref': 'datastore-678',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'santosh_rcg3_ds1',
          'moref': 'datastore-665',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'Datastore',
          'moref': 'datastore-185',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': '13_DS1',
          'moref': 'datastore-673',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': '27_JAN_DS2',
          'moref': 'datastore-680',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_9',
          'moref': 'datastore-289',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'datastore1 (1)',
          'moref': 'datastore-660',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_3',
          'moref': 'datastore-14',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS2',
          'moref': 'datastore-668',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_RC_1',
          'moref': 'datastore-584',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s747',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_1_renamed',
          'moref': 'datastore-281',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS1',
          'moref': 'datastore-667',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_5',
          'moref': 'datastore-285',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s751',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_2',
          'moref': 'datastore-13',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': '12_DS1',
          'moref': 'datastore-670',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-p745',
            'type': 'storagePod'
          }
        },
        {
          'name': 'DS_4',
          'moref': 'datastore-15',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'santosh_rcg4_ds1',
          'moref': 'datastore-666',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'snap-3bae8518-12_DS1',
          'moref': 'datastore-676',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_3',
          'moref': 'datastore-283',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-s748',
            'type': 'datastore'
          }
        },
        {
          'name': 'snap-38c8414c-12_DS1',
          'moref': 'datastore-677',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'snap-1a3a8b86-12_DS2',
          'moref': 'datastore-675',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        },
        {
          'name': 'DS_Shared_4',
          'moref': 'datastore-284',
          'type': 'VMFS',
          'status': 'Ok',
          'state': 'Ok',
          'stateReason': '',
          'host': [
            'host-9'
          ],
          'parent': {
            'moref': 'group-p766',
            'type': 'storagePod'
          }
        },
        {
          'name': '12_DS2',
          'moref': 'datastore-671',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-p745',
            'type': 'storagePod'
          }
        },
        {
          'name': 'DSRMCDEPLOY',
          'moref': 'datastore-663',
          'type': 'VMFS',
          'status': 'Error',
          'state': 'Unavailable',
          'stateReason': '',
          'host': [
            'host-657'
          ],
          'parent': {
            'moref': 'group-s5',
            'type': 'datastore'
          }
        }
      ],
      'vms': [
        {
          'name': 'vm2_ds3_no_disk',
          'moref': 'vm-37',
          'uuid': '4209008d-e96b-16f5-9d01-fe16522a8de3',
          'instanceUuid': '5009e644-2d77-ad4e-1a89-7f83b85d3773',
          'vmxConfigPath': '[DS_3] vm2_ds3_no_disk/vm2_ds3_no_disk.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-14'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': None,
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [

          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'vm3_ds3_multi_disk_diff_ds_with_rdms',
          'moref': 'vm-39',
          'uuid': '4209d1c3-cdb3-ccb5-af68-ad5fdb7ce7dd',
          'instanceUuid': '5009ee36-0e48-ce58-37bd-9d87358c0916',
          'vmxConfigPath': '[DS_3] vm3_ds3_multi_disk_diff_ds_with_rdms/vm3_ds3_multi_disk_diff_ds_with_rdms.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-14',
            'datastore-15'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2008 R2 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-14',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '192-2000',
              'uid': '6000C298-d87c-1d0a-44f8-b3518dd93993',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_3] vm3_ds3_multi_disk_diff_ds_with_rdms/vm3_ds3_multi_disk_diff_ds_with_rdms.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-15',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '192-2001',
              'uid': '6000C298-2723-41c2-6302-168f495d2973',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_4] vm3_ds3_multi_disk_diff_ds_with_rdms/vm3_ds3_multi_disk_diff_ds_with_rdms.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 23622320128,
              'datastore': 'datastore-14',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '192-2002',
              'uid': '6000C295-f3d4-eb81-5389-e92413913cb8',
              'type': 'VRDM',
              'backingFileInfo': {
                'filePath': '[DS_3] vm3_ds3_multi_disk_diff_ds_with_rdms/vm3_ds3_multi_disk_diff_ds_with_rdms_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'santosh_rcg4_vm1',
          'moref': 'vm-684',
          'uuid': '4231436d-3a83-22d7-303a-affd3a84c0e4',
          'instanceUuid': '5031faa5-dacf-7f4f-17be-7c0f2eee808c',
          'vmxConfigPath': '[santosh_rcg4_ds1] santosh_rcg4_vm1/santosh_rcg4_vm1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-666'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-666',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '11-2000',
              'uid': '6000C298-b93a-7fa8-f546-c498be3d18e9',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[santosh_rcg4_ds1] santosh_rcg4_vm1/santosh_rcg4_vm1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2012.4',
          'moref': 'vm-715',
          'uuid': '4231564e-9245-c240-5fff-b039cfe8a250',
          'instanceUuid': '5031fee7-80bf-1a69-0fab-42617ebed763',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2012.4/atlas-1.0.0-2012.4.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '62-2000',
              'uid': '6000C29d-bc65-1ef8-a9e7-4924452f6b11',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2012.4/atlas-1.0.0-2012.4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Jul-10-2019-17-08-50',
          'moref': 'vm-682',
          'uuid': '4231b320-4521-38c5-7dc7-61d636630437',
          'instanceUuid': '50312a2a-bed8-3b05-ef6a-5d0bcc809c41',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-Jul-10-2019-17-08-50/rmc-Jul-10-2019-17-08-50.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10245',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '10-2000',
              'uid': '6000C29a-4c34-eafd-393b-4bca35e9f10e',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-Jul-10-2019-17-08-50/rmc-Jul-10-2019-17-08-50.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-py3_san_1947.1',
          'moref': 'vm-703',
          'uuid': '42310c01-667e-01fd-179e-c0e0f6a1d055',
          'instanceUuid': '503180cb-f457-cf63-730b-1c86cbf604e7',
          'vmxConfigPath': '[RMCDEPLOY2] rmc-py3_san_1947.1/rmc-py3_san_1947.1.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '48-2000',
              'uid': '6000C290-3941-faad-8702-ba255c5baf91',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] rmc-py3_san_1947.1/rmc-py3_san_1947.1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': '27_JAN_VM1',
          'moref': 'vm-711',
          'uuid': '4231a8c0-f644-b23f-21f0-98352a7fe53d',
          'instanceUuid': '50319a70-2c55-2096-34cd-32663fd2f4be',
          'vmxConfigPath': '[27_JAN_DS] 27_JAN_VM1/27_JAN_VM1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-679'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 21474836480,
              'datastore': 'datastore-679',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '57-2000',
              'uid': '6000C291-c676-40cf-2a58-500cadf6a980',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[27_JAN_DS] 27_JAN_VM1/27_JAN_VM1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Sep-27-2019-6-2-GA',
          'moref': 'vm-581',
          'uuid': '421503a0-0e34-28d2-aeab-f51c4695b195',
          'instanceUuid': '5015c285-245c-a780-d5e9-d53bcaf29507',
          'vmxConfigPath': '[DS_RMC_OVF] rmc-Sep-27-2019-6-2-GA/rmc-Sep-27-2019-6-2-GA.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-11'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': 'CentOS 6 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-11',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '332-2000',
              'uid': '6000C29a-647e-662d-b8f1-5a51e87aaae4',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_RMC_OVF] rmc-Sep-27-2019-6-2-GA/rmc-Sep-27-2019-6-2-GA.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Oct-18-2019-11-58-01_6.2_105',
          'moref': 'vm-692',
          'uuid': '42313bf8-99a0-968e-3506-02460230fe7d',
          'instanceUuid': '5031e979-8994-1df2-9ea0-6aaf7385f478',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-Oct-18-2019-11-58-01/rmc-Oct-18-2019-11-58-01.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '39-2000',
              'uid': '6000C297-0957-c3d8-ca2b-ec8642b7f13d',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-Oct-18-2019-11-58-01/rmc-Oct-18-2019-11-58-01.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm_event_1',
          'moref': 'vm-651',
          'uuid': '42151e26-9e1e-5ea8-7c17-620d80b3715f',
          'instanceUuid': '50158717-3428-9583-035c-6aba7bbda6ea',
          'vmxConfigPath': '[DS_3] vm_event_1/vm_event_1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-14'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 1073741824,
              'datastore': 'datastore-14',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '366-2000',
              'uid': '6000C298-d908-66cc-9c7f-288230e981fe',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_3] vm_event_1/vm_event_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'resgroup-v746',
            'type': 'vapp'
          }
        },
        {
          'name': 'atlas-1.0.0-2013.12',
          'moref': 'vm-718',
          'uuid': '4231ec4b-4722-4c67-6764-8b4387497f02',
          'instanceUuid': '5031309d-730b-fd3a-911f-bb6e16db448a',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2013.12/atlas-1.0.0-2013.12.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '66-2000',
              'uid': '6000C299-a5d9-01dc-80b0-e0194efbc343',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2013.12/atlas-1.0.0-2013.12.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm1_ds2',
          'moref': 'vm-216',
          'uuid': '4215e4c4-e48b-ab67-2d44-2055d70db930',
          'instanceUuid': '50159515-6f20-133b-a2c7-d6633519c947',
          'vmxConfigPath': '[DS_2] vm1_ds2/vm1_ds2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-13'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-13',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '250-2000',
              'uid': '6000C294-8d29-7e98-5e57-5d4740627731',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_2] vm1_ds2/vm1_ds2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-dev_6.3.0-1950.2',
          'moref': 'vm-709',
          'uuid': '42313082-d958-4853-f7c2-928cdc7846e4',
          'instanceUuid': '5031fd92-1316-78d2-dac5-88cd5c696bb6',
          'vmxConfigPath': '[RMCDEPLOY2] rmc-dev_6.3.0-1950.2/rmc-dev_6.3.0-1950.2.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '51-2000',
              'uid': '6000C295-3d15-2399-9d59-766581a302c7',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] rmc-dev_6.3.0-1950.2/rmc-dev_6.3.0-1950.2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'SAN_NEW_VM',
          'moref': 'vm-691',
          'uuid': '564df635-10ea-ea44-ee5b-f1e9b18cc3e9',
          'instanceUuid': '528e4eeb-5653-4605-75d8-cfbf9ef44f80',
          'vmxConfigPath': '[San_28AUG_DS] SAN_NEW_VM/SAN_NEW_VM.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-669'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeMSI',
            'version': '9349',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 107374182400,
              'datastore': 'datastore-669',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '37-2000',
              'uid': '6000C29d-1f2c-a955-f6bc-dfc8ca8329b2',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[San_28AUG_DS] SAN_NEW_VM/SAN_NEW_VM.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 16106127360,
              'datastore': 'datastore-669',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '37-2001',
              'uid': None,
              'type': 'PRDM',
              'backingFileInfo': {
                'filePath': '[San_28AUG_DS] SAN_NEW_VM/SAN_NEW_VM_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'vmdkDiskMode': 'independent_persistent'
              }
            },
            {
              'capacityInBytes': 16106127360,
              'datastore': 'datastore-669',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '37-2002',
              'uid': '6000C294-f5b4-e053-53fc-7a0609eb5c50',
              'type': 'VRDM',
              'backingFileInfo': {
                'filePath': '[San_28AUG_DS] SAN_NEW_VM/SAN_NEW_VM_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2012.4_san',
          'moref': 'vm-716',
          'uuid': '42312cac-ba17-0b92-f5eb-eb52504d90cd',
          'instanceUuid': '503155f6-641a-d655-11fc-1f42c9dc4096',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2012.4_san/atlas-1.0.0-2012.4_san.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '63-2000',
              'uid': '6000C29e-c6e2-0348-c68f-929254803c3b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2012.4_san/atlas-1.0.0-2012.4_san.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2028.8',
          'moref': 'vm-735',
          'uuid': '423efec8-cf45-9a81-e88a-cc82887d81b1',
          'instanceUuid': '503eb779-381a-3bed-685f-1c6537f68e65',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2028.8/atlas-1.0.0-2028.8.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '85-2000',
              'uid': '6000C295-2be0-f00b-9a42-c5cee92e83cb',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2028.8/atlas-1.0.0-2028.8.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm_shared_10_ds',
          'moref': 'vm-291',
          'uuid': '42158556-824e-4c72-40ed-9d37786a147e',
          'instanceUuid': '5015b836-3b9e-9597-c8c2-b1e771c6822e',
          'vmxConfigPath': '[DS_Shared_1_renamed] vm_shared_10_ds/vm_shared_10_ds.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-281',
            'datastore-282',
            'datastore-283',
            'datastore-284',
            'datastore-285',
            'datastore-286',
            'datastore-287',
            'datastore-288',
            'datastore-289',
            'datastore-290'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-281',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '259-2000',
              'uid': '6000C29d-60a1-967f-5b68-dad8a1c3c0f6',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_1_renamed] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-282',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '259-2001',
              'uid': '6000C29f-7d9c-edda-44c7-27f696b49003',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_2] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-283',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '259-2002',
              'uid': '6000C29e-f2b1-9614-c899-b832413236ce',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_3] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 8589934592,
              'datastore': 'datastore-284',
              'name': 'Hard disk 4',
              'controllerKey': 1000,
              'key': 2003,
              'unitNumber': 3,
              'diskObjectId': '259-2003',
              'uid': '6000C29c-f6f5-24b3-d219-d13237ebc423',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_4] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-285',
              'name': 'Hard disk 5',
              'controllerKey': 1000,
              'key': 2004,
              'unitNumber': 4,
              'diskObjectId': '259-2004',
              'uid': '6000C298-61dd-ad8d-8336-fa602899d5fa',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_5] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-286',
              'name': 'Hard disk 6',
              'controllerKey': 1000,
              'key': 2005,
              'unitNumber': 5,
              'diskObjectId': '259-2005',
              'uid': '6000C293-a704-478d-dbbc-bf6db9408ec0',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_6] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-287',
              'name': 'Hard disk 7',
              'controllerKey': 1000,
              'key': 2006,
              'unitNumber': 6,
              'diskObjectId': '259-2006',
              'uid': '6000C29d-3723-9fd0-e7be-4066dbee89ad',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_7] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 8589934592,
              'datastore': 'datastore-288',
              'name': 'Hard disk 8',
              'controllerKey': 1000,
              'key': 2008,
              'unitNumber': 8,
              'diskObjectId': '259-2008',
              'uid': '6000C298-8cc3-87fa-cae3-66fb6d2bd190',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_8] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-289',
              'name': 'Hard disk 9',
              'controllerKey': 1000,
              'key': 2009,
              'unitNumber': 9,
              'diskObjectId': '259-2009',
              'uid': '6000C29e-e8e9-a161-8d1c-53343b27f465',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_9] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 8589934592,
              'datastore': 'datastore-290',
              'name': 'Hard disk 10',
              'controllerKey': 1000,
              'key': 2010,
              'unitNumber': 10,
              'diskObjectId': '259-2010',
              'uid': '6000C292-3baa-bf50-3933-584b7bb06db1',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_10] vm_shared_10_ds/vm_shared_10_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'VM1',
          'moref': 'vm-687',
          'uuid': '4231e601-fb93-66a0-a80c-115e33c1559a',
          'instanceUuid': 'd0483150-aeec-86a1-8142-36607756e2f2',
          'vmxConfigPath': '[DS1] clone_VM1_20190828114834/clone_VM1_20190828114834.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-667',
            'datastore-668'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-667',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '22-2000',
              'uid': '6000C292-aa71-2a25-6779-a71728a760a0',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS1] clone_VM1_20190828114834/clone_VM1_20190828114834_4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 5368709120,
              'datastore': 'datastore-667',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '22-2001',
              'uid': None,
              'type': 'PRDM',
              'backingFileInfo': {
                'filePath': '[DS1] clone_VM1_20190828114834/clone_VM1_20190828114834_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'vmdkDiskMode': 'independent_persistent'
              }
            },
            {
              'capacityInBytes': 5368709120,
              'datastore': 'datastore-667',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '22-2002',
              'uid': '6000C299-1165-6476-0d7d-49aac96b3f32',
              'type': 'VRDM',
              'backingFileInfo': {
                'filePath': '[DS1] clone_VM1_20190828114834/clone_VM1_20190828114834_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'vmdkDiskMode': 'independent_persistent'
              }
            },
            {
              'capacityInBytes': 16106127360,
              'datastore': 'datastore-667',
              'name': 'Hard disk 4',
              'controllerKey': 1000,
              'key': 2003,
              'unitNumber': 3,
              'diskObjectId': '22-2003',
              'uid': '6000C290-24e6-1f6e-2b9c-808bb6281ab9',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS1] clone_VM1_20190828114834/clone_VM1_20190828114834_3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 9663676416,
              'datastore': 'datastore-668',
              'name': 'Hard disk 5',
              'controllerKey': 1000,
              'key': 2004,
              'unitNumber': 4,
              'diskObjectId': '22-2004',
              'uid': '6000C298-aa03-ccd1-b1a9-4bc07acccb90',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS2] VM3/VM3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': '12_DS2_VM1',
          'moref': 'vm-696',
          'uuid': '423111aa-64f2-3854-b525-a1a687950ce0',
          'instanceUuid': '5031d672-978c-a167-ea5a-6891cffd5281',
          'vmxConfigPath': '[12_DS2] 12_DS2_VM1/12_DS2_VM1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-671',
            'datastore-676'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-671',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '42-2000',
              'uid': '6000C290-2a27-ecc2-7f88-1a16eddda75d',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[12_DS2] 12_DS2_VM1/12_DS2_VM1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-676',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '42-2001',
              'uid': '6000C29f-e19f-df62-d918-897ac8cc7c3a',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[snap-3bae8518-12_DS1] 12_DS1_vm2/12_DS1_vm2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '1024',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm_to_restore',
          'moref': 'vm-495',
          'uuid': '421597de-9df2-240a-d8a1-8fce20df214f',
          'instanceUuid': 'b2331550-c8ad-e4c9-1a8e-bc9cc91876af',
          'vmxConfigPath': '[DS_Shared_1_renamed] clone_vm_to_restore_20190802064839/clone_vm_to_restore_20190802064839.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-281'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-281',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '273-2000',
              'uid': '6000C29a-ef03-1d20-b705-e257099aa06a',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_1_renamed] clone_vm_to_restore_20190802064839/clone_vm_to_restore_20190802064839.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'non_3par_vm',
          'moref': 'vm-21',
          'uuid': '42092a6c-865d-6b55-319c-6c6aa2794d1f',
          'instanceUuid': '5009599b-93a0-3cab-ebc7-5946e47840a7',
          'vmxConfigPath': '[datastore1 (2)] non_3par_vm/non_3par_vm.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-10'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-10',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '132-2000',
              'uid': '6000C290-400d-45f7-b5a6-73b344328973',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (2)] non_3par_vm/non_3par_vm.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-dev_6.3.0-1947.5',
          'moref': 'vm-705',
          'uuid': '4231f2f5-1921-7bca-d550-f49ecd9209e1',
          'instanceUuid': '5031e05a-7278-d3be-15f9-b28a2e802f93',
          'vmxConfigPath': '[RMCDEPLOY2] rmc-dev_6.3.0-1947.5/rmc-dev_6.3.0-1947.5.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '49-2000',
              'uid': '6000C292-36e8-e27e-cd1c-78636b6fb10a',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] rmc-dev_6.3.0-1947.5/rmc-dev_6.3.0-1947.5.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm1_ds1_rc',
          'moref': 'vm-585',
          'uuid': '4215261f-7b8f-e8f6-0485-905f8d43949d',
          'instanceUuid': '5015bd6c-a4d7-48ab-fac3-c31196826beb',
          'vmxConfigPath': '[DS_RC_1] vm1_ds1_rc/vm1_ds1_rc.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-584'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-584',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '335-2000',
              'uid': '6000C294-f223-8f36-1f5d-9873ac94e8b4',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_RC_1] vm1_ds1_rc/vm1_ds1_rc.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v744',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2019.6',
          'moref': 'vm-729',
          'uuid': '423e97ab-6aea-8174-ad4a-1cb05cf6c5fc',
          'instanceUuid': '503e9ef4-5742-e35b-7d44-30071c7e388a',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2019.6/atlas-1.0.0-2019.6.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '78-2000',
              'uid': '6000C29f-5771-8e81-a215-1e2cde06bf9a',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2019.6/atlas-1.0.0-2019.6.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm2_ds1_rc',
          'moref': 'vm-586',
          'uuid': '42152b90-009e-f304-655b-c672b048e1b7',
          'instanceUuid': '50154ba8-6fef-d862-01da-4119035bee20',
          'vmxConfigPath': '[DS_RC_1] vm2_ds1_rc/vm2_ds1_rc.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-584'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-584',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '336-2000',
              'uid': '6000C290-77bc-0787-38b3-8cc5b7acb60c',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_RC_1] vm2_ds1_rc/vm2_ds1_rc.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v744',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Jul-10-2019-15-47-46',
          'moref': 'vm-737',
          'uuid': '42316842-8790-2b8a-d2ce-dab3028e2140',
          'instanceUuid': '503108be-8214-0a26-bf90-95c19039ebec',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-Jul-10-2019-15-47-46/rmc-Jul-10-2019-15-47-46.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10245',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '9-2000',
              'uid': '6000C296-53a8-bb84-1789-cf8c1f7ac254',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-Jul-10-2019-15-47-46/rmc-Jul-10-2019-15-47-46.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'Windows_2008_vcenter',
          'moref': 'vm-46',
          'uuid': '564de5e1-33d8-4e34-3183-bda8aae4c80b',
          'instanceUuid': '52a1cb0a-3da8-d785-8766-a2e3889b6d91',
          'vmxConfigPath': '[datastore1 (2)] Windows_2008_vcenter/Windows_2008_vcenter.vmx',
          'diskUuidEnabled': True,
          'powerState': 'On',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-10'
          ],
          'networkAddress': '172.17.29.71',
          'toolsInfo': {
            'type': 'guestToolsTypeMSI',
            'version': '9349',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2008 R2 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 107374182400,
              'datastore': 'datastore-10',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '231-2000',
              'uid': '6000C293-f114-8532-d786-c327ca030294',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (2)] Windows_2008_vcenter/Windows_2008_vcenter.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'vm_ds_shared_2',
          'moref': 'vm-522',
          'uuid': '42155279-cde2-a8cd-46ad-f14476f5124c',
          'instanceUuid': '5015572a-d2af-a3de-4ad0-ba63c156d1e3',
          'vmxConfigPath': '[DS_Shared_2] vm_ds_shared_2/vm_ds_shared_2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-282'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-282',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '287-2000',
              'uid': '6000C29c-f804-0e4d-8373-e2e044d04db6',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_Shared_2] vm_ds_shared_2/vm_ds_shared_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Apr-30-2020-11-46-10',
          'moref': 'vm-725',
          'uuid': '423e16eb-220a-272a-42d4-2c723fea96d0',
          'instanceUuid': '503e1868-bc45-f5a9-87a6-d4592e8adbe2',
          'vmxConfigPath': '[RMCDEPLOY2] rmc-Apr-30-2020-11-46-10/rmc-Apr-30-2020-11-46-10.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': '172.17.29.107',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 6 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '74-2000',
              'uid': '6000C291-4bc1-c05a-ed75-171a674425ca',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] rmc-Apr-30-2020-11-46-10/rmc-Apr-30-2020-11-46-10.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'VM3',
          'moref': 'vm-688',
          'uuid': '42319dbe-f9cb-8ac0-8231-bd24f739be36',
          'instanceUuid': '5031498a-e637-caa0-f0e6-0b65cb24d760',
          'vmxConfigPath': '[DS2] VM3/VM3.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-668'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 9663676416,
              'datastore': 'datastore-668',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '25-2000',
              'uid': '6000C298-aa03-ccd1-b1a9-4bc07acccb90',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS2] VM3/VM3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rcgroup_vm3',
          'moref': 'vm-693',
          'uuid': '4216f463-fe76-39a8-9ee0-fc556995eb74',
          'instanceUuid': '5016033f-eb15-2015-9790-bd139d8f2fcc',
          'vmxConfigPath': '[rcgroup_ds2] rcgroup_vm3/rcgroup_vm3.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-662'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 5368709120,
              'datastore': 'datastore-662',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '4-2000',
              'uid': '6000C294-b04c-ed90-1c4a-28d89d7e9e80',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds2] rcgroup_vm3/rcgroup_vm3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '512',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm1_ds3',
          'moref': 'vm-36',
          'uuid': '420919fa-b976-e089-c57a-aced10d1990c',
          'instanceUuid': '500915d6-65cb-0904-1ac0-1762e4117808',
          'vmxConfigPath': '[DS_3] vm1_ds3/vm1_ds3.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-14'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2008 R2 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-14',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '188-2000',
              'uid': '6000C295-bb69-b070-aa5e-1ff0a4323251',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_3] vm1_ds3/vm1_ds3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 1073741824,
              'datastore': 'datastore-14',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '188-2001',
              'uid': '6000C29e-8423-6ec3-4f7d-b95f381ea85b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_3] vm1_ds3/vm1_ds3_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-14',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '188-2002',
              'uid': '6000C29c-c6de-c913-80d7-fc3d354e25db',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_3] vm1_ds3/vm1_ds3_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2028.8_san',
          'moref': 'vm-736',
          'uuid': '423e6009-13fb-3a89-8477-f68bd08c1d6f',
          'instanceUuid': '503e015f-d8e6-2972-608d-717d758036c5',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2028.8_san/atlas-1.0.0-2028.8_san.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': '172.17.29.105',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '86-2000',
              'uid': '6000C290-a157-1791-090f-317af77f4fe5',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2028.8_san/atlas-1.0.0-2028.8_san.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': '12_DS1_vm2',
          'moref': 'vm-710',
          'uuid': '42317978-898d-c540-345e-a01c02c8b4d0',
          'instanceUuid': '50310387-2e31-44dd-da51-9458e6439f5e',
          'vmxConfigPath': '[12_DS1] 12_DS1_vm2/12_DS1_vm2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-670',
            'datastore-671'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-670',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '52-2000',
              'uid': '6000C29f-e19f-df62-d918-897ac8cc7c3a',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[12_DS1] 12_DS1_vm2/12_DS1_vm2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-671',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '52-2001',
              'uid': '6000C29d-bb9f-b868-a6a1-4d338c803128',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[12_DS2] 12_DS1_vm2/12_DS1_vm2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-py3_san_6_3.0-1943.4_27.160',
          'moref': 'vm-702',
          'uuid': '4231505c-3f19-d307-8f0c-4fd5fdf5afdf',
          'instanceUuid': '503131e7-070a-73fb-f202-1b43496185a0',
          'vmxConfigPath': '[RMCDEPLOY2] rmc-py3_san_6_3.0-1943.4_27.160/rmc-py3_san_6_3.0-1943.4_27.160.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '47-2000',
              'uid': '6000C29d-f011-54a7-2725-ab18bdd47823',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] rmc-py3_san_6_3.0-1943.4_27.160/rmc-py3_san_6_3.0-1943.4_27.160.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm2_ds1',
          'moref': 'vm-583',
          'uuid': '4215de6c-8dea-d959-1048-ac3275d4f25a',
          'instanceUuid': '50155eb8-54af-e8fe-71f2-b452a2c0edd9',
          'vmxConfigPath': '[DS_1] vm2_ds1/vm2_ds1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-12'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-12',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '334-2000',
              'uid': '6000C29b-ab7b-dbd1-2961-49b7162d6f5e',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_1] vm2_ds1/vm2_ds1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'Atlas_74',
          'moref': 'vm-646',
          'uuid': '4215ad99-b6f3-2aee-9b61-7fafe7bb0748',
          'instanceUuid': '5015e050-945b-fc16-482b-73a6f9b70cc4',
          'vmxConfigPath': '[DS_RMC_OVF] Atlas_74/Atlas_74.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-11'
          ],
          'networkAddress': '172.17.29.74',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-11',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '360-2000',
              'uid': '6000C295-ffbe-044d-802e-28b43691d22f',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_RMC_OVF] Atlas_74/Atlas_74.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'vm1_ds4_renamed',
          'moref': 'vm-30',
          'uuid': '42094c56-1cce-676d-63ba-0adeb0765734',
          'instanceUuid': '500961e5-a85e-bdc9-97a8-b8f567ee6886',
          'vmxConfigPath': '[DS_4] vm1_ds4/vm1_ds4.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-15'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2008 R2 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-15',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '180-2000',
              'uid': '6000C290-a451-9fc3-be6f-28ded6b47b95',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_4] vm1_ds4/vm1_ds4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': '13_DS1_VM1',
          'moref': 'vm-698',
          'uuid': '42317608-119c-9c2e-7455-156005b84854',
          'instanceUuid': '50314f02-d58d-f76f-c370-80c3735db04f',
          'vmxConfigPath': '[13_DS1] 13_DS1_VM1/13_DS1_VM1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-673'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-673',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '43-2000',
              'uid': '6000C29a-722a-96ad-cc15-c0b2165dd9c6',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[13_DS1] 13_DS1_VM1/13_DS1_VM1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '1024',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2014.1',
          'moref': 'vm-719',
          'uuid': '42318727-8869-2ba8-f22e-346c46c02738',
          'instanceUuid': '5031308f-f174-1f80-c75d-5df9f2324a8e',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2014.1/atlas-1.0.0-2014.1.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '67-2000',
              'uid': '6000C290-e051-dd03-e447-416b0b00faf2',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2014.1/atlas-1.0.0-2014.1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'SANTOSH_VCSA6.7',
          'moref': 'vm-723',
          'uuid': '564da774-057c-15dd-b46b-bc5ccf45c441',
          'instanceUuid': '52cbd6c2-52f0-ec5b-62fe-f8a85961c276',
          'vmxConfigPath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-660'
          ],
          'networkAddress': '172.17.29.103',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10304',
            'installed': True
          },
          'guestInfo': {
            'name': 'VMware Photon OS (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 12884901888,
              'datastore': 'datastore-660',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '70-2000',
              'uid': '6000C290-9afc-b476-01d1-20eb136e19c4',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 1849688064,
              'datastore': 'datastore-660',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '70-2001',
              'uid': '6000C299-8702-6988-cb5d-6ef3748a7c1f',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 26843545600,
              'datastore': 'datastore-660',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '70-2002',
              'uid': '6000C295-550b-6ac7-4a17-f1f068142a7b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 26843545600,
              'datastore': 'datastore-660',
              'name': 'Hard disk 4',
              'controllerKey': 1000,
              'key': 2003,
              'unitNumber': 3,
              'diskObjectId': '70-2003',
              'uid': '6000C29c-284b-e7c6-df3c-2aa988572e07',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-660',
              'name': 'Hard disk 5',
              'controllerKey': 1000,
              'key': 2004,
              'unitNumber': 4,
              'diskObjectId': '70-2004',
              'uid': '6000C29b-83d4-6853-3d1a-6526d47a98c7',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-660',
              'name': 'Hard disk 6',
              'controllerKey': 1000,
              'key': 2005,
              'unitNumber': 5,
              'diskObjectId': '70-2005',
              'uid': '6000C290-a03a-131d-5855-1a2991cb3f7a',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_5.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 16106127360,
              'datastore': 'datastore-660',
              'name': 'Hard disk 7',
              'controllerKey': 1000,
              'key': 2006,
              'unitNumber': 6,
              'diskObjectId': '70-2006',
              'uid': '6000C298-8848-7fbe-eaa7-0c3d85583170',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_6.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-660',
              'name': 'Hard disk 8',
              'controllerKey': 1000,
              'key': 2008,
              'unitNumber': 8,
              'diskObjectId': '70-2008',
              'uid': '6000C290-da6e-ec32-9326-72904d51ade5',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_7.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 1073741824,
              'datastore': 'datastore-660',
              'name': 'Hard disk 9',
              'controllerKey': 1000,
              'key': 2009,
              'unitNumber': 9,
              'diskObjectId': '70-2009',
              'uid': '6000C29e-b95c-a6b3-0c35-76c460d0d34f',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_8.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-660',
              'name': 'Hard disk 10',
              'controllerKey': 1000,
              'key': 2010,
              'unitNumber': 10,
              'diskObjectId': '70-2010',
              'uid': '6000C293-4d21-f1f5-d613-8fcea9606b3e',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_9.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-660',
              'name': 'Hard disk 11',
              'controllerKey': 1000,
              'key': 2011,
              'unitNumber': 11,
              'diskObjectId': '70-2011',
              'uid': '6000C291-1469-1741-b9f0-4127c3b815ce',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_10.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 107374182400,
              'datastore': 'datastore-660',
              'name': 'Hard disk 12',
              'controllerKey': 1000,
              'key': 2012,
              'unitNumber': 12,
              'diskObjectId': '70-2012',
              'uid': '6000C291-5ce8-c9b0-6722-93f5f8c0f08e',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_11.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 53687091200,
              'datastore': 'datastore-660',
              'name': 'Hard disk 13',
              'controllerKey': 1000,
              'key': 2013,
              'unitNumber': 13,
              'diskObjectId': '70-2013',
              'uid': '6000C29e-a1d9-45cf-865a-f2b336c219fe',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SANTOSH_VCSA6.7/SANTOSH_VCSA6.7_12.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '10240',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm3_ds2_multi_disk_same_ds',
          'moref': 'vm-34',
          'uuid': '4209aef5-e9e8-23ef-24e4-2156732ba809',
          'instanceUuid': '50094307-b546-e6e2-e3f1-fa0b43517ae3',
          'vmxConfigPath': '[DS_2] vm3_ds2_multi_disk_same_ds/vm3_ds2_multi_disk_same_ds.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-13',
            'datastore-514'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 6442450944,
              'datastore': 'datastore-13',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '186-2000',
              'uid': '6000C29c-cc4a-d8a7-01d6-c284b13fce93',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_2] vm3_ds2_multi_disk_same_ds/vm3_ds2_multi_disk_same_ds.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-13',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '186-2001',
              'uid': '6000C296-942a-2270-a10d-b529c32099aa',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_2] vm3_ds2_multi_disk_same_ds/vm3_ds2_multi_disk_same_ds_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 0,
              'datastore': 'datastore-514',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '186-2002',
              'uid': None,
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[snap-33772199-ANUP_NEW_TEST_DS] ANUP_NEW_TEST_VM1/ANUP_NEW_TEST_VM1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'santosh_rmcv_rcg_vm',
          'moref': 'vm-689',
          'uuid': '4216306d-b6b6-f1fe-43d1-a703ea85111d',
          'instanceUuid': '50163823-406c-69cb-54fc-2e82676a07ee',
          'vmxConfigPath': '[santosh_rmcv_rcg_ds] santosh_rmcv_rcg_vm/santosh_rmcv_rcg_vm.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-664'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-664',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '3-2000',
              'uid': '6000C295-cd46-a7bd-1b34-3f48241d56e7',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[santosh_rmcv_rcg_ds] santosh_rmcv_rcg_vm/santosh_rmcv_rcg_vm.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Oct-18-2019-12-28-55',
          'moref': 'vm-694',
          'uuid': '42312c37-c98f-c054-9538-9834bf916dd5',
          'instanceUuid': '50310ac7-ff2a-47ed-7b44-39df7a0736b0',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-Oct-18-2019-12-28-55/rmc-Oct-18-2019-12-28-55.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeUnknown',
            'version': '2147483647',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '40-2000',
              'uid': '6000C290-0bfa-5d6f-b039-c657f2488d6f',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-Oct-18-2019-12-28-55/rmc-Oct-18-2019-12-28-55.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-May-16-2019-12-56-14',
          'moref': 'vm-721',
          'uuid': '42161087-3caf-303f-cbbf-04be99eb2d88',
          'instanceUuid': '5016f20d-c647-5c83-e945-f8045c9ae1f9',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-May-16-2019-12-56-14/rmc-May-16-2019-12-56-14.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeUnknown',
            'version': '2147483647',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '7-2000',
              'uid': '6000C29c-a445-ebcc-ce7f-174385fb9b9f',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-May-16-2019-12-56-14/rmc-May-16-2019-12-56-14.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rcgroup_vm1_2',
          'moref': 'vm-727',
          'uuid': '423ec384-5df7-aded-cd90-4c856243bc9d',
          'instanceUuid': '503ee8a0-909a-c50a-3990-fb3b5c2856ab',
          'vmxConfigPath': '[rcgroup_ds1] rcgroup_vm1_2/rcgroup_vm1_2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-661',
            'datastore-670'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-661',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '76-2000',
              'uid': '6000C297-b5db-244b-86f9-8b11dbeb0a96',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds1] rcgroup_vm1_2/rcgroup_vm1_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-670',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '76-2001',
              'uid': '6000C290-a750-a792-c7e2-e134de5de544',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[12_DS1] rcgroup_vm1_2/rcgroup_vm1_2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': '27_JAN_VM2',
          'moref': 'vm-712',
          'uuid': '4231ccfb-8a8e-4d46-13b4-7eb2fc9e569f',
          'instanceUuid': '50315480-cb52-df35-a731-929122b17b99',
          'vmxConfigPath': '[27_JAN_DS2] 27_JAN_VM2/27_JAN_VM2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-680'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 16106127360,
              'datastore': 'datastore-680',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '58-2000',
              'uid': '6000C297-b810-7a78-65ce-8587c29935c4',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[27_JAN_DS2] 27_JAN_VM2/27_JAN_VM2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2014.9',
          'moref': 'vm-724',
          'uuid': '423e77f9-c7f3-1022-c6cf-aab6d8b57e53',
          'instanceUuid': '503e2e22-58da-ed42-ba0b-0b03aad5376b',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2014.9/atlas-1.0.0-2014.9.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': '172.17.29.104',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '71-2000',
              'uid': '6000C29a-00e0-e7e4-c0d5-d3ad7cf523f5',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2014.9/atlas-1.0.0-2014.9.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm_event',
          'moref': 'vm-650',
          'uuid': '4215d13a-5a1c-6bac-4a80-f4905c25c2a9',
          'instanceUuid': '5015aece-548c-9957-6a28-4c738fe8241c',
          'vmxConfigPath': '[DS_2] vm_event/vm_event.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-13'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 1073741824,
              'datastore': 'datastore-13',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '365-2000',
              'uid': '6000C299-2919-8ee7-6341-3462c47704fc',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_2] vm_event/vm_event.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'resgroup-v746',
            'type': 'vapp'
          }
        },
        {
          'name': 'santosh_rcg3_vm1',
          'moref': 'vm-685',
          'uuid': '4231ea6d-e8b1-15c3-9746-834977b19b82',
          'instanceUuid': '5031a0b6-c46e-a33f-4285-5cf5e64aa39e',
          'vmxConfigPath': '[santosh_rcg3_ds1] santosh_rcg3_vm1/santosh_rcg3_vm1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-665'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-665',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '2-2000',
              'uid': '6000C295-fd90-5aa2-d5a1-b700f42de329',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[santosh_rcg3_ds1] santosh_rcg3_vm1/santosh_rcg3_vm1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2010.1_san',
          'moref': 'vm-713',
          'uuid': '42316cd1-1a19-66e3-5344-c46a7f1ab325',
          'instanceUuid': '503178ae-2b8e-95d2-6f36-376163c29efe',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2010.1_san/atlas-1.0.0-2010.1_san.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '61-2000',
              'uid': '6000C292-fe72-d574-107a-b295ef48ed4b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2010.1_san/atlas-1.0.0-2010.1_san.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'Atlas_76',
          'moref': 'vm-649',
          'uuid': '42156310-ed53-707b-a02f-c8979ec6632b',
          'instanceUuid': '5015d035-30f5-4d93-2553-b05b4f89350f',
          'vmxConfigPath': '[DS_RMC_OVF] Atlas_76/Atlas_76.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-11'
          ],
          'networkAddress': '172.17.29.76',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-11',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '364-2000',
              'uid': '6000C291-f25d-1bed-0f07-113da96010e5',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_RMC_OVF] Atlas_76/Atlas_76.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'rcgroup_vm1_1',
          'moref': 'vm-726',
          'uuid': '423eda12-01e6-e4b6-6d4b-14d3055276df',
          'instanceUuid': '503e9cad-23ac-95f6-2f38-7f806b6d3ca1',
          'vmxConfigPath': '[rcgroup_ds1] rcgroup_vm1_1/rcgroup_vm1_1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-661'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-661',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '75-2000',
              'uid': '6000C298-d97b-be91-a45c-8e2b26f25edb',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds1] rcgroup_vm1_1/rcgroup_vm1_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 41943040,
              'datastore': 'datastore-661',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '75-2001',
              'uid': '6000C292-2fba-92b0-d3b9-3a4823ce67a9',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds1] rcgroup_vm1_1/rcgroup_vm1_1_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'py3_clone',
          'moref': 'vm-701',
          'uuid': '42313b4a-125d-7285-0761-4ce5ca6d8c9f',
          'instanceUuid': '50315f76-b484-4516-29b1-d02c2769301d',
          'vmxConfigPath': '[RMCDEPLOY2] py3_clone/py3_clone.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeUnknown',
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '46-2000',
              'uid': '6000C291-19ac-fa89-614e-5090767ff0f1',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] py3_clone/py3_clone.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': '12_DS1_VM1',
          'moref': 'vm-695',
          'uuid': '4231fd30-76aa-073f-17ef-e2edc6d49519',
          'instanceUuid': '50318e59-086e-3eca-b5de-e57d3eb0618c',
          'vmxConfigPath': '[12_DS1] 12_DS1_VM1/12_DS1_VM1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-670'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-670',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '41-2000',
              'uid': '6000C290-e29f-16ca-fc01-208b86471a55',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[12_DS1] 12_DS1_VM1/12_DS1_VM1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '1024',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'VM2',
          'moref': 'vm-686',
          'uuid': '4231bb37-7e16-66bb-3558-92710ccdafdf',
          'instanceUuid': '5031a5d6-6772-d5be-909e-d37032bc2617',
          'vmxConfigPath': '[DS2] VM2/VM2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-668'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 16106127360,
              'datastore': 'datastore-668',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '20-2000',
              'uid': '6000C290-24e6-1f6e-2b9c-808bb6281ab9',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS2] VM2/VM2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'VM_Demo',
          'moref': 'vm-187',
          'uuid': '4215c00e-46b0-087e-703e-84b9b039f3e2',
          'instanceUuid': '5015c595-3d48-9d09-5dae-e7b71f742423',
          'vmxConfigPath': '[Demo_DS] VM_Demo/VM_Demo.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-186',
            'datastore-502'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-186',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '243-2000',
              'uid': '6000C291-47a2-354d-6c76-71ce0a8e0c50',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[Demo_DS] VM_Demo/VM_Demo.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 0,
              'datastore': 'datastore-502',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '243-2001',
              'uid': None,
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[snap-5fe6b284-DS_Shared_1] DLT_VM_TEST/DLT_VM_TEST.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'vm1_ds1',
          'moref': 'vm-582',
          'uuid': '42156430-3fe0-1910-150c-16e30f625e42',
          'instanceUuid': '50153800-a481-322b-7038-bfbe8115cd7a',
          'vmxConfigPath': '[DS_1] vm1_ds1/vm1_ds1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-12'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-12',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '333-2000',
              'uid': '6000C29d-c975-535e-0c4f-814b015e0bf4',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_1] vm1_ds1/vm1_ds1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 1073741824,
              'datastore': 'datastore-12',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '333-2001',
              'uid': '6000C291-237b-1da2-d850-5d74a085db87',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_1] vm1_ds1/vm1_ds1_3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-12',
              'name': 'Hard disk 3',
              'controllerKey': 1000,
              'key': 2002,
              'unitNumber': 2,
              'diskObjectId': '333-2002',
              'uid': '6000C293-472d-7b7c-abbb-7853e6dccc0d',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_1] vm1_ds1/vm1_ds1_4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2014.5',
          'moref': 'vm-720',
          'uuid': '4231332e-c085-7020-d9b8-fcdd50e81f6a',
          'instanceUuid': '5031ce27-11fb-11b9-4865-32f44b3eb630',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2014.5/atlas-1.0.0-2014.5.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '69-2000',
              'uid': '6000C296-1966-d12b-4374-9d3628d7627b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2014.5/atlas-1.0.0-2014.5.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': '13_DS2_VM1',
          'moref': 'vm-699',
          'uuid': '4231e59c-3cdd-3089-8677-41f30bd50017',
          'instanceUuid': '503126ee-69a6-7ebc-5d88-d397ae9a3f4f',
          'vmxConfigPath': '[13_DS2] 13_DS2_VM1/13_DS2_VM1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-672'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 2147483648,
              'datastore': 'datastore-672',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '44-2000',
              'uid': '6000C294-4be7-caa1-d546-44a657d94b5b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[13_DS2] 13_DS2_VM1/13_DS2_VM1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '1024',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rcgroup_vm1',
          'moref': 'vm-707',
          'uuid': '42168f37-a118-2bd0-9b01-c8fd2f0f90d1',
          'instanceUuid': '5016bfec-2a3b-50f5-471e-98059cc50df8',
          'vmxConfigPath': '[rcgroup_ds1] rcgroup_vm1/rcgroup_vm1.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-661'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 5368709120,
              'datastore': 'datastore-661',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '5-2000',
              'uid': '6000C296-2f26-5b25-a07f-9eb0bdf223ae',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds1] rcgroup_vm1/rcgroup_vm1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '512',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-dev_6.3.0-1949.3_110',
          'moref': 'vm-708',
          'uuid': '4231e3a8-ff1e-5543-c820-43e8220e9d09',
          'instanceUuid': '50317030-c8a4-cba4-4b67-e472c06cfb67',
          'vmxConfigPath': '[RMCDEPLOY2] rmc-dev_6.3.0-1949.3_110/rmc-dev_6.3.0-1949.3_110.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '50-2000',
              'uid': '6000C29e-5690-47d7-8a61-e9792c072f01',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] rmc-dev_6.3.0-1949.3_110/rmc-dev_6.3.0-1949.3_110.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-py3_santosh_6_3.0-1943.4_27.160',
          'moref': 'vm-700',
          'uuid': '4231ab68-ae5d-250d-03cf-6ed27ce9fc95',
          'instanceUuid': '503141ba-bad9-1dfa-8315-18d0d53cea4e',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-py3_santosh_6_3.0-1943.4_27.160/rmc-py3_santosh_6_3.0-1943.4_27.160.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10309',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '45-2000',
              'uid': '6000C296-e51c-d706-6afa-9f7110fd5b54',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-py3_santosh_6_3.0-1943.4_27.160/rmc-py3_santosh_6_3.0-1943.4_27.160.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'vm2_ds2',
          'moref': 'vm-33',
          'uuid': '4209e9c6-5a5d-cd44-5e32-70ccb6bcd79a',
          'instanceUuid': '5009daed-70b6-30e3-96bf-b309385c9c18',
          'vmxConfigPath': '[DS_2] vm2_ds2/vm2_ds2.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Ok',
          'host': 'host-9',
          'datastore': [
            'datastore-13'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2008 R2 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 4294967296,
              'datastore': 'datastore-13',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '185-2000',
              'uid': '6000C290-b851-e20d-274b-0ea9c5599f6b',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DS_2] vm2_ds2/vm2_ds2.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 1,
            'num_cpu_threads': 1
          },
          'parent': {
            'moref': 'group-v3',
            'type': 'vm'
          }
        },
        {
          'name': 'rmc-Mar-25-2019-16-46-09_106',
          'moref': 'vm-731',
          'uuid': '4216de86-db21-0f78-07e8-b297b282fa7a',
          'instanceUuid': '50162186-46f0-d39b-b801-af82a0c56c3f',
          'vmxConfigPath': '[DSRMCDEPLOY] rmc-Mar-25-2019-16-46-09/rmc-Mar-25-2019-16-46-09.vmx',
          'diskUuidEnabled': False,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-663'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10245',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-663',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '8-2000',
              'uid': '6000C29e-0618-cdf9-446f-6c99a23b6ac2',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[DSRMCDEPLOY] rmc-Mar-25-2019-16-46-09/rmc-Mar-25-2019-16-46-09.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '16384',
            'num_cpu_cores': 4,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'rcgroup_vm1_3',
          'moref': 'vm-728',
          'uuid': '423eeda7-8899-f48f-442c-196ca4dcad1f',
          'instanceUuid': '503e12b4-2204-afd3-f9d1-9978b08f8013',
          'vmxConfigPath': '[rcgroup_ds1] rcgroup_vm1_3/rcgroup_vm1_3.vmx',
          'diskUuidEnabled': True,
          'powerState': 'Off',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-661'
          ],
          'networkAddress': None,
          'toolsInfo': {
            'type': None,
            'version': '0',
            'installed': False
          },
          'guestInfo': {
            'name': None
          },
          'vmdks': [
            {
              'capacityInBytes': 1073741824,
              'datastore': 'datastore-661',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '77-2000',
              'uid': '6000C295-f95a-1dd9-727a-fdcd34c47172',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds1] rcgroup_vm1_3/rcgroup_vm1_3.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': False,
                'vmdkDiskMode': 'persistent'
              }
            },
            {
              'capacityInBytes': 10737418240,
              'datastore': 'datastore-661',
              'name': 'Hard disk 2',
              'controllerKey': 1000,
              'key': 2001,
              'unitNumber': 1,
              'diskObjectId': '77-2001',
              'uid': None,
              'type': 'PRDM',
              'backingFileInfo': {
                'filePath': '[rcgroup_ds1] rcgroup_vm1_3/rcgroup_vm1_3_1.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'vmdkDiskMode': 'independent_persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '4096',
            'num_cpu_cores': 2,
            'num_cpu_threads': 4
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2020.4',
          'moref': 'vm-730',
          'uuid': '423e519e-8980-c87d-d2a9-7fb9dfa2886d',
          'instanceUuid': '503ef4dc-46c6-4610-be41-41a506268164',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2020.4/atlas-1.0.0-2020.4.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': '172.17.29.106',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '79-2000',
              'uid': '6000C29b-7b44-f027-3718-012ad002345f',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2020.4/atlas-1.0.0-2020.4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2029.4',
          'moref': 'vm-734',
          'uuid': '423e37aa-402a-bdf8-b645-cd883a41ea66',
          'instanceUuid': '503ecd3c-e1e8-63d8-d01a-5bd8ed0d88f5',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2029.4/atlas-1.0.0-2029.4.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': '172.17.29.110',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '84-2000',
              'uid': '6000C29b-c7e2-810a-2a95-fc6e1006d734',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2029.4/atlas-1.0.0-2029.4.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'SantoshVC',
          'moref': 'vm-681',
          'uuid': '564d87e1-afb9-4462-2825-a229f604c1d2',
          'instanceUuid': '522ed07a-b94f-defd-a984-1821c94c752e',
          'vmxConfigPath': '[datastore1 (1)] SantoshVC/SantoshVC.vmx',
          'diskUuidEnabled': True,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-660'
          ],
          'networkAddress': '172.17.29.101',
          'toolsInfo': {
            'type': 'guestToolsTypeMSI',
            'version': '9349',
            'installed': False
          },
          'guestInfo': {
            'name': 'Microsoft Windows Server 2012 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 107374182400,
              'datastore': 'datastore-660',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '1-2000',
              'uid': '6000C29b-d99c-0eae-171b-f12cc8b3e682',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[datastore1 (1)] SantoshVC/SantoshVC.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '36864',
            'num_cpu_cores': 4,
            'num_cpu_threads': 8
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        },
        {
          'name': 'atlas-1.0.0-2024.5',
          'moref': 'vm-733',
          'uuid': '423e3037-a9db-82c5-ea1f-a4d6669cc11c',
          'instanceUuid': '503ecd52-5a71-ae16-7b03-e1375caf7371',
          'vmxConfigPath': '[RMCDEPLOY2] atlas-1.0.0-2024.5/atlas-1.0.0-2024.5.vmx',
          'diskUuidEnabled': False,
          'powerState': 'On',
          'status': 'Error',
          'host': 'host-657',
          'datastore': [
            'datastore-674'
          ],
          'networkAddress': '172.17.29.102',
          'toolsInfo': {
            'type': 'guestToolsTypeOpenVMTools',
            'version': '10336',
            'installed': True
          },
          'guestInfo': {
            'name': 'CentOS 7 (64-bit)'
          },
          'vmdks': [
            {
              'capacityInBytes': 214748364800,
              'datastore': 'datastore-674',
              'name': 'Hard disk 1',
              'controllerKey': 1000,
              'key': 2000,
              'unitNumber': 0,
              'diskObjectId': '83-2000',
              'uid': '6000C293-613a-c20d-3b67-d42de860b350',
              'type': 'VMFS',
              'backingFileInfo': {
                'filePath': '[RMCDEPLOY2] atlas-1.0.0-2024.5/atlas-1.0.0-2024.5.vmdk',
                'vmdkSharingMode': 'sharingNone',
                'isThinDisk': True,
                'vmdkDiskMode': 'persistent'
              }
            }
          ],
          'computeInfo': {
            'memory_size': '8192',
            'num_cpu_cores': 2,
            'num_cpu_threads': 2
          },
          'parent': {
            'moref': 'group-v654',
            'type': 'vm'
          }
        }
      ],
      'folders': [
        {
          'name': 'Datastore_Cluster_1',
          'moref': 'group-p745',
          'type': 'storagePod',
          'parent': 'group-s5'
        },
        {
          'name': 'Datastore_Folder_1',
          'moref': 'group-s743',
          'parent': 'group-s5',
          'type': 'datastore',
          'sub_folder': [
            {
              'name': 'Datastore_Folder_sub_1',
              'moref': 'group-s747',
              'parent': 'group-s743',
              'type': 'datastore',
              'sub_folder': [
                {
                  'name': 'Datastore_Folder_sub_1_1',
                  'moref': 'group-s749',
                  'parent': 'group-s747',
                  'type': 'datastore',
                  'sub_folder': [

                  ],
                  'ds_list': [

                  ],
                  'vm_list': [

                  ]
                }
              ],
              'ds_list': [

              ],
              'vm_list': [

              ]
            },
            {
              'name': 'Datastore_Folder_sub_2',
              'moref': 'group-s748',
              'parent': 'group-s743',
              'type': 'datastore',
              'sub_folder': [
                {
                  'name': 'Datastore_cluster_inside_sub_2',
                  'moref': 'group-p766',
                  'type': 'storagePod',
                  'parent': 'group-s748'
                }
              ],
              'ds_list': [

              ],
              'vm_list': [

              ]
            }
          ],
          'ds_list': [

          ],
          'vm_list': [

          ]
        },
        {
          'name': 'Datastore_Folder_2',
          'moref': 'group-s751',
          'parent': 'group-s5',
          'type': 'datastore',
          'sub_folder': [

          ],
          'ds_list': [

          ],
          'vm_list': [

          ]
        },
        {
          'name': 'Discovered virtual machine',
          'moref': 'group-v654',
          'parent': 'group-v3',
          'type': 'vm',
          'sub_folder': [

          ],
          'ds_list': [

          ],
          'vm_list': [

          ]
        },
        {
          'name': 'VM_Folder_1',
          'moref': 'group-v744',
          'parent': 'group-v3',
          'type': 'vm',
          'sub_folder': [
            {
              'name': 'vapp_2',
              'moref': 'resgroup-v750',
              'type': 'vapp',
              'parent': 'group-v744'
            }
          ],
          'ds_list': [

          ],
          'vm_list': [

          ]
        },
        {
          'name': 'vapp_1',
          'moref': 'resgroup-v746',
          'type': 'vapp',
          'parent': 'group-v3'
        },
        {
          'name': 'Host_Cluster_1',
          'moref': 'domain-c652',
          'type': 'cluster',
          'parent': 'group-h4'
        },
        {
          'name': 'Host_Cluster_2',
          'moref': 'domain-c741',
          'type': 'cluster',
          'parent': 'group-h740'
        }
      ]
    }
  ]
}