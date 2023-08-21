# One DS belogs to multiple hosts
BUILD_SAMPLE3 = {
  'id': 'd8deb0f7-5822-408d-816b-0bd621271375',
  'name': 'vcenter1',
  'datacenters': [
    {
      'name': 'Datacenter1',
      'moref': 'datacenter-1',
      'clusters': [
        {
          'name': 'Cluster1',
          'moref': 'domain-c1',
          'hosts': [
            {
              'name': 'Host1',
              'moref': 'host-1',
              'datastores': [
                {
                  'name': 'Datastore1',
                  'moref': 'ds-1',
                  'folder': {
                    'moref': 'group-s1',
                    'name': 'dsFolder1'
                  },
                  'vms': [
                    {
                      'name': 'vm1',
                      'moref': 'vm-1',
                      'folder': {
                        'moref': 'group-1',
                        'name': 'vmFolder1'
                      }
                    },
                    {
                      'name': 'vm2',
                      'moref': 'vm-2',
                      'folder': {
                        'moref': 'group-1',
                        'name': 'vmFolder1'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore2',
                  'moref': 'ds-2',
                  'folder': {
                    'moref': 'group-s1',
                    'name': 'dsFolder1'
                  },
                  'vms': [
                    {
                      'name': 'vm3',
                      'moref': 'vm-3',
                      'folder': {
                        'moref': 'group-1',
                        'name': 'vmFolder1'
                      }
                    },
                    {
                      'name': 'vm4',
                      'moref': 'vm-4',
                      'folder': {
                        'moref': 'group-1',
                        'name': 'vmFolder1'
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Host2',
              'moref': 'host-2',
              'datastores': [
                {
                  'name': 'Datastore1',
                  'moref': 'ds-1',
                  'folder': {
                    'moref': 'group-s1',
                    'name': 'dsFolder1'
                  },
                  'vms': [
                    {
                      'name': 'vm1',
                      'moref': 'vm-1',
                      'folder': {
                        'moref': 'group-1',
                        'name': 'vmFolder1'
                      }
                    },
                    {
                      'name': 'vm2',
                      'moref': 'vm-2',
                      'folder': {
                        'moref': 'group-1',
                        'name': 'vmFolder1'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore3',
                  'moref': 'ds-3',
                  'folder': {
                    'moref': 'group-s2',
                    'name': 'dsFolder2'
                  },
                  'vms': [
                    {
                      'name': 'vm5',
                      'moref': 'vm-5',
                      'folder': {
                        'moref': 'group-2',
                        'name': 'vmFolder2'
                      }
                    },
                    {
                      'name': 'vm6',
                      'moref': 'vm-6',
                      'folder': {
                        'moref': 'group-2',
                        'name': 'vmFolder2'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore4',
                  'moref': 'ds-4',
                  'folder': {
                    'moref': 'group-s2',
                    'name': 'dsFolder2'
                  },
                  'vms': [
                    {
                      'name': 'vm7',
                      'moref': 'vm-7',
                      'folder': {
                        'moref': 'group-2',
                        'name': 'vmFolder2'
                      }
                    },
                    {
                      'name': 'vm8',
                      'moref': 'vm-8',
                      'folder': {
                        'moref': 'group-2',
                        'name': 'vmFolder2'
                      }
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'Cluster2',
          'moref': 'domain-c2',
          'hosts': [
            {
              'name': 'Host3',
              'moref': 'host-3',
              'datastores': [
                {
                  'name': 'Datastore5',
                  'moref': 'ds-5',
                  'folder': {
                    'moref': 'group-s3',
                    'name': 'dsFolder3'
                  },
                  'vms': [
                    {
                      'name': 'vm9',
                      'moref': 'vm-9',
                      'folder': {
                        'moref': 'group-3',
                        'name': 'vmFolder3'
                      }
                    },
                    {
                      'name': 'vm10',
                      'moref': 'vm-10',
                      'folder': {
                        'moref': 'group-3',
                        'name': 'vmFolder3'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore6',
                  'moref': 'ds-6',
                  'folder': {
                    'moref': 'group-s3',
                    'name': 'dsFolder3'
                  },
                  'vms': [
                    {
                      'name': 'vm11',
                      'moref': 'vm-11',
                      'folder': {
                        'moref': 'group-3',
                        'name': 'vmFolder3'
                      }
                    },
                    {
                      'name': 'vm12',
                      'moref': 'vm-12',
                      'folder': {
                        'moref': 'group-3',
                        'name': 'vmFolder3'
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Host4',
              'moref': 'host-4',
              'datastores': [
                {
                  'name': 'Datastore7',
                  'moref': 'ds-7',
                  'folder': {
                    'moref': 'group-s4',
                    'name': 'dsFolder4'
                  },
                  'vms': [
                    {
                      'name': 'vm13',
                      'moref': 'vm-13',
                      'folder': {
                        'moref': 'group-4',
                        'name': 'vmFolder4'
                      }
                    },
                    {
                      'name': 'vm14',
                      'moref': 'vm-14',
                      'folder': {
                        'moref': 'group-4',
                        'name': 'vmFolder4'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore8',
                  'moref': 'ds-8',
                  'folder': {
                    'moref': 'group-s4',
                    'name': 'dsFolder4'
                  },
                  'vms': [
                    {
                      'name': 'vm15',
                      'moref': 'vm-15',
                      'folder': {
                        'moref': 'group-4',
                        'name': 'vmFolder4'
                      }
                    },
                    {
                      'name': 'vm16',
                      'moref': 'vm-16',
                      'folder': {
                        'moref': 'group-4',
                        'name': 'vmFolder4'
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      'name': 'Datacenter2',
      'moref': 'datacenter-2',
      'clusters': [
        {
          'name': 'Cluster3',
          'moref': 'domain-c3',
          'hosts': [
            {
              'name': 'Host5',
              'moref': 'host-5',
              'datastores': [
                {
                  'name': 'Datastore9',
                  'moref': 'ds-9',
                  'folder': {
                    'moref': 'group-s5',
                    'name': 'dsFolder5'
                  },
                  'vms': [
                    {
                      'name': 'vm17',
                      'moref': 'vm-17',
                      'folder': {
                        'moref': 'group-5',
                        'name': 'vmFolder5'
                      }
                    },
                    {
                      'name': 'vm18',
                      'moref': 'vm-18',
                      'folder': {
                        'moref': 'group-5',
                        'name': 'vmFolder5'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore10',
                  'moref': 'ds-10',
                  'folder': {
                    'moref': 'group-s5',
                    'name': 'dsFolder5'
                  },
                  'vms': [
                    {
                      'name': 'vm19',
                      'moref': 'vm-19',
                      'folder': {
                        'moref': 'group-5',
                        'name': 'vmFolder5'
                      }
                    },
                    {
                      'name': 'vm20',
                      'moref': 'vm-20',
                      'folder': {
                        'moref': 'group-5',
                        'name': 'vmFolder5'
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Host6',
              'moref': 'host-6',
              'datastores': [
                {
                  'name': 'Datastore11',
                  'moref': 'ds-11',
                  'folder': {
                    'moref': 'group-s6',
                    'name': 'dsFolder6'
                  },
                  'vms': [
                    {
                      'name': 'vm21',
                      'moref': 'vm-21',
                      'folder': {
                        'moref': 'group-6',
                        'name': 'vmFolder6'
                      }
                    },
                    {
                      'name': 'vm22',
                      'moref': 'vm-22',
                      'folder': {
                        'moref': 'group-6',
                        'name': 'vmFolder6'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore12',
                  'moref': 'ds-12',
                  'folder': {
                    'moref': 'group-s6',
                    'name': 'dsFolder6'
                  },
                  'vms': [
                    {
                      'name': 'vm23',
                      'moref': 'vm-23',
                      'folder': {
                        'moref': 'group-6',
                        'name': 'vmFolder6'
                      }
                    },
                    {
                      'name': 'vm24',
                      'moref': 'vm-24',
                      'folder': {
                        'moref': 'group-6',
                        'name': 'vmFolder6'
                      }
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          'name': 'Cluster4',
          'moref': 'domain-c4',
          'hosts': [
            {
              'name': 'Host7',
              'moref': 'host-7',
              'datastores': [
                {
                  'name': 'Datastore13',
                  'moref': 'ds-13',
                  'folder': {
                    'moref': 'group-s7',
                    'name': 'dsFolder7'
                  },
                  'vms': [
                    {
                      'name': 'vm25',
                      'moref': 'vm-25',
                      'folder': {
                        'moref': 'group-7',
                        'name': 'vmFolder7'
                      }
                    },
                    {
                      'name': 'vm26',
                      'moref': 'vm-26',
                      'folder': {
                        'moref': 'group-7',
                        'name': 'vmFolder7'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore14',
                  'moref': 'ds-14',
                  'folder': {
                    'moref': 'group-s7',
                    'name': 'dsFolder7'
                  },
                  'vms': [
                    {
                      'name': 'vm27',
                      'moref': 'vm-27',
                      'folder': {
                        'moref': 'group-7',
                        'name': 'vmFolder7'
                      }
                    },
                    {
                      'name': 'vm28',
                      'moref': 'vm-28',
                      'folder': {
                        'moref': 'group-7',
                        'name': 'vmFolder7'
                      }
                    }
                  ]
                }
              ]
            },
            {
              'name': 'Host8',
              'moref': 'host-8',
              'datastores': [
                {
                  'name': 'Datastore15',
                  'moref': 'ds-15',
                  'folder': {
                    'moref': 'group-s8',
                    'name': 'dsFolder8'
                  },
                  'vms': [
                    {
                      'name': 'vm29',
                      'moref': 'vm-29',
                      'folder': {
                        'moref': 'group-8',
                        'name': 'vmFolder8'
                      }
                    },
                    {
                      'name': 'vm30',
                      'moref': 'vm-30',
                      'folder': {
                        'moref': 'group-8',
                        'name': 'vmFolder8'
                      }
                    }
                  ]
                },
                {
                  'name': 'Datastore16',
                  'moref': 'ds-16',
                  'folder': {
                    'moref': 'group-s8',
                    'name': 'dsFolder8'
                  },
                  'vms': [
                    {
                      'name': 'vm31',
                      'moref': 'vm-31',
                      'folder': {
                        'moref': 'group-8',
                        'name': 'vmFolder8'
                      }
                    },
                    {
                      'name': 'vm32',
                      'moref': 'vm-32',
                      'folder': {
                        'moref': 'group-8',
                        'name': 'vmFolder8'
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}