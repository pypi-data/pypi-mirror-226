BUILD_SAMPLE4 = {
  'id': 'd8deb0f7-5822-408d-816b-0bd621271375',
  'name': 'vcenter1',
  'datacenters': [
    {
      'name': 'Datacenter1',
      'moref': 'datacenter-1',
      'folders': [
        {
          'name': 'vmFolder1',
          'moref': 'group-1',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder1)',
              'moref': 'group-2',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder1',
                'moref': 'group-1'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder1))',
                  'moref': 'group-3',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder1)',
                    'moref': 'group-2'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder1)',
              'moref': 'group-4',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder1',
                'moref': 'group-1'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder1))',
                  'moref': 'group-5',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder1)',
                    'moref': 'group-4'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'vmFolder2',
          'moref': 'group-6',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder2)',
              'moref': 'group-7',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder2',
                'moref': 'group-6'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder2))',
                  'moref': 'group-8',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder2)',
                    'moref': 'group-7'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder2)',
              'moref': 'group-9',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder2',
                'moref': 'group-6'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder2))',
                  'moref': 'group-10',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder2)',
                    'moref': 'group-9'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'vmFolder3',
          'moref': 'group-11',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder3)',
              'moref': 'group-12',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder3',
                'moref': 'group-11'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder3))',
                  'moref': 'group-13',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder3)',
                    'moref': 'group-12'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder3)',
              'moref': 'group-14',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder3',
                'moref': 'group-11'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder3))',
                  'moref': 'group-15',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder3)',
                    'moref': 'group-14'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'vmFolder4',
          'moref': 'group-16',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder4)',
              'moref': 'group-17',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder4',
                'moref': 'group-16'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder4))',
                  'moref': 'group-18',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder4)',
                    'moref': 'group-17'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder4)',
              'moref': 'group-19',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder4',
                'moref': 'group-16'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder4))',
                  'moref': 'group-20',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder4)',
                    'moref': 'group-19'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder1',
          'moref': 'group-s1',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder1)',
              'moref': 'group-s2',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder1',
                'moref': 'group-s1'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder1))',
                  'moref': 'group-s3',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder1)',
                    'moref': 'group-s2'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder1)',
              'moref': 'group-s4',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder1',
                'moref': 'group-s1'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder1))',
                  'moref': 'group-s5',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder1)',
                    'moref': 'group-s4'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder2',
          'moref': 'group-s6',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder2)',
              'moref': 'group-s7',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder2',
                'moref': 'group-s6'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder2))',
                  'moref': 'group-s8',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder2)',
                    'moref': 'group-s7'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder2)',
              'moref': 'group-s9',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder2',
                'moref': 'group-s6'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder2))',
                  'moref': 'group-s10',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder2)',
                    'moref': 'group-s9'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder3',
          'moref': 'group-s11',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder3)',
              'moref': 'group-s12',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder3',
                'moref': 'group-s11'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder3))',
                  'moref': 'group-s13',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder3)',
                    'moref': 'group-s12'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder3)',
              'moref': 'group-s14',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder3',
                'moref': 'group-s11'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder3))',
                  'moref': 'group-s15',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder3)',
                    'moref': 'group-s14'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder4',
          'moref': 'group-s16',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder4)',
              'moref': 'group-s17',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder4',
                'moref': 'group-s16'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder4))',
                  'moref': 'group-s18',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder4)',
                    'moref': 'group-s17'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder4)',
              'moref': 'group-s19',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder4',
                'moref': 'group-s16'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder4))',
                  'moref': 'group-s20',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder4)',
                    'moref': 'group-s19'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        }
      ],
      'hosts': [
        {
          'name': 'Host1',
          'moref': 'host-1',
          'datastores': [
            {
              'name': 'Datastore1',
              'moref': 'datastore-1',
              'folder': 'group-s1',
              'vms': [
                {
                  'name': 'vm1',
                  'moref': 'vm-1',
                  'folder': 'group-1',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2001',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-1',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore1/vm1.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm2',
                  'moref': 'vm-2',
                  'folder': 'group-1',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2002',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-1',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore1/vm2.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Datastore2',
              'moref': 'datastore-2',
              'folder': 'group-s1',
              'vms': [
                {
                  'name': 'vm3',
                  'moref': 'vm-3',
                  'folder': 'group-1',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2003',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-2',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore2/vm3.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm4',
                  'moref': 'vm-4',
                  'folder': 'group-1',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2004',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-2',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore2/vm4.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            }
          ],
          'cluster': {
            'name': 'Cluster1',
            'moref': 'domain-c1'
          }
        },
        {
          'name': 'Host2',
          'moref': 'host-2',
          'datastores': [
            {
              'name': 'Datastore3',
              'moref': 'datastore-3',
              'folder': 'group-s2',
              'vms': [
                {
                  'name': 'vm5',
                  'moref': 'vm-5',
                  'folder': 'group-2',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2005',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-3',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore3/vm5.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm6',
                  'moref': 'vm-6',
                  'folder': 'group-2',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2006',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-3',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore3/vm6.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Datastore4',
              'moref': 'datastore-4',
              'folder': 'group-s2',
              'vms': [
                {
                  'name': 'vm7',
                  'moref': 'vm-7',
                  'folder': 'group-2',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2007',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-4',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore4/vm7.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm8',
                  'moref': 'vm-8',
                  'folder': 'group-2',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2008',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-4',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore4/vm8.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            }
          ],
          'cluster': {
            'name': 'Cluster1',
            'moref': 'domain-c1'
          }
        }
      ]
    },
    {
      'name': 'Datacenter2',
      'moref': 'datacenter-2',
      'folders': [
        {
          'name': 'vmFolder1',
          'moref': 'group-21',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder1)',
              'moref': 'group-22',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder1',
                'moref': 'group-21'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder1))',
                  'moref': 'group-23',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder1)',
                    'moref': 'group-22'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder1)',
              'moref': 'group-24',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder1',
                'moref': 'group-21'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder1))',
                  'moref': 'group-25',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder1)',
                    'moref': 'group-24'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'vmFolder2',
          'moref': 'group-26',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder2)',
              'moref': 'group-27',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder2',
                'moref': 'group-26'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder2))',
                  'moref': 'group-28',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder2)',
                    'moref': 'group-27'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder2)',
              'moref': 'group-29',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder2',
                'moref': 'group-26'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder2))',
                  'moref': 'group-30',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder2)',
                    'moref': 'group-29'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'vmFolder3',
          'moref': 'group-31',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder3)',
              'moref': 'group-32',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder3',
                'moref': 'group-31'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder3))',
                  'moref': 'group-33',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder3)',
                    'moref': 'group-32'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder3)',
              'moref': 'group-34',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder3',
                'moref': 'group-31'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder3))',
                  'moref': 'group-35',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder3)',
                    'moref': 'group-34'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'vmFolder4',
          'moref': 'group-36',
          'type': 'vm',
          'parent': {
            'name': 'vm'
          },
          'sub_folder': [
            {
              'name': 'sf1(vmFolder4)',
              'moref': 'group-37',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder4',
                'moref': 'group-36'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(vmFolder4))',
                  'moref': 'group-38',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf1(vmFolder4)',
                    'moref': 'group-37'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(vmFolder4)',
              'moref': 'group-39',
              'type': 'vm',
              'parent': {
                'name': 'vmFolder4',
                'moref': 'group-36'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(vmFolder4))',
                  'moref': 'group-40',
                  'type': 'vm',
                  'parent': {
                    'name': 'sf2(vmFolder4)',
                    'moref': 'group-39'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder1',
          'moref': 'group-s21',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder1)',
              'moref': 'group-s22',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder1',
                'moref': 'group-s21'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder1))',
                  'moref': 'group-s23',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder1)',
                    'moref': 'group-s22'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder1)',
              'moref': 'group-s24',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder1',
                'moref': 'group-s21'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder1))',
                  'moref': 'group-s25',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder1)',
                    'moref': 'group-s24'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder2',
          'moref': 'group-s26',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder2)',
              'moref': 'group-s27',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder2',
                'moref': 'group-s26'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder2))',
                  'moref': 'group-s28',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder2)',
                    'moref': 'group-s27'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder2)',
              'moref': 'group-s29',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder2',
                'moref': 'group-s26'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder2))',
                  'moref': 'group-s30',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder2)',
                    'moref': 'group-s29'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder3',
          'moref': 'group-s31',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder3)',
              'moref': 'group-s32',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder3',
                'moref': 'group-s31'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder3))',
                  'moref': 'group-s33',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder3)',
                    'moref': 'group-s32'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder3)',
              'moref': 'group-s34',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder3',
                'moref': 'group-s31'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder3))',
                  'moref': 'group-s35',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder3)',
                    'moref': 'group-s34'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'dsFolder4',
          'moref': 'group-s36',
          'type': 'datastore',
          'parent': {
            'name': 'datastore'
          },
          'sub_folder': [
            {
              'name': 'sf1(dsFolder4)',
              'moref': 'group-s37',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder4',
                'moref': 'group-s36'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf1(dsFolder4))',
                  'moref': 'group-s38',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf1(dsFolder4)',
                    'moref': 'group-s37'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            },
            {
              'name': 'sf2(dsFolder4)',
              'moref': 'group-s39',
              'type': 'datastore',
              'parent': {
                'name': 'dsFolder4',
                'moref': 'group-s36'
              },
              'sub_folder': [
                {
                  'name': 'ssf1(sf2(dsFolder4))',
                  'moref': 'group-s40',
                  'type': 'datastore',
                  'parent': {
                    'name': 'sf2(dsFolder4)',
                    'moref': 'group-s39'
                  },
                  'sub_folder': [

                  ]
                }
              ]
            }
          ]
        }
      ],
      'hosts': [
        {
          'name': 'Host3',
          'moref': 'host-3',
          'datastores': [
            {
              'name': 'Datastore5',
              'moref': 'datastore-5',
              'folder': 'group-s3',
              'vms': [
                {
                  'name': 'vm9',
                  'moref': 'vm-9',
                  'folder': 'group-3',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-2009',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-5',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore5/vm9.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm10',
                  'moref': 'vm-10',
                  'folder': 'group-3',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20010',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-5',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore5/vm10.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Datastore6',
              'moref': 'datastore-6',
              'folder': 'group-s3',
              'vms': [
                {
                  'name': 'vm11',
                  'moref': 'vm-11',
                  'folder': 'group-3',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20011',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-6',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore6/vm11.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm12',
                  'moref': 'vm-12',
                  'folder': 'group-3',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20012',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-6',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore6/vm12.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            }
          ],
          'cluster': {
            'name': 'Cluster2',
            'moref': 'domain-c2'
          }
        },
        {
          'name': 'Host4',
          'moref': 'host-4',
          'datastores': [
            {
              'name': 'Datastore7',
              'moref': 'datastore-7',
              'folder': 'group-s4',
              'vms': [
                {
                  'name': 'vm13',
                  'moref': 'vm-13',
                  'folder': 'group-4',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20013',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-7',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore7/vm13.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm14',
                  'moref': 'vm-14',
                  'folder': 'group-4',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20014',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-7',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore7/vm14.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Datastore8',
              'moref': 'datastore-8',
              'folder': 'group-s4',
              'vms': [
                {
                  'name': 'vm15',
                  'moref': 'vm-15',
                  'folder': 'group-4',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20015',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-8',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore8/vm15.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                },
                {
                  'name': 'vm16',
                  'moref': 'vm-16',
                  'folder': 'group-4',
                  'vmdks': [
                    {
                      'controllerKey': 1000,
                      'controllerType': 'VirtualLsiLogicController',
                      'controllerSharingMode': 'noSharing',
                      'key': 2000,
                      'unitNumber': 0,
                      'diskObjectId': '70-20016',
                      'capacityInBytes': 12884901888,
                      'backingId': '6000C2909afcb47601d120eb136e19c4',
                      'datastore': 'datastore-8',
                      'backingFileInfo': {
                        'type': 'VirtualDiskFlatVer2',
                        'isRDM': False,
                        'vmdkPath': 'Datastore8/vm16.vmdk',
                        'compatibilityMode': None,
                        'vmdkSharingMode': 'sharingNone',
                        'isThinDisk': True,
                        'vmdkDiskMode': 'persistent',
                        'isAccessible': True
                      }
                    }
                  ]
                }
              ]
            }
          ],
          'cluster': {
            'name': 'Cluster2',
            'moref': 'domain-c2'
          }
        }
      ]
    }
  ]
}