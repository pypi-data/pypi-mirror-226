import logging
LOG = logging.getLogger(__name__)

def recursive_asdict(d):
    """Convert Suds object into serializable format used to convert config object."""
    out = {}
    #LOG.info('#################inside recursive_asdict d: {0}'.format(d))
    #LOG.info('#################inside recursive_asdict type(d): {0}'.format(type(d)))

    if d is None:
        return d

    #print (d)
    #print(type(d))
    #LOG.info('#################inside d.__dict__: {0}'.format(d.__dict__))
    for k, v in d.items():
        #LOG.info('#################inside recursive_asdict v: {0}'.format(v))
        if k== 'device':
            LOG.info('#################device: {0}'.format(v))
            LOG.info('#################device: {0}'.format(isinstance(v, list)))
        if k in ['dynamicType', 'dynamicProperty']:
            continue
        if isinstance(v, dict):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if isinstance(item, dict):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out


if __name__ =='__main__':
    d = {
      'VirtualDisk': {
        'backing': {
          'parent': {
            'parent': {
              'parent': {
                'parent': {
                  'parent': {
                    'parent': {
                      'parent': {
                        'parent': {
                          'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                          'diskMode': 'persistent',
                          'contentId': '1cf528f9b287bf902f29c42fffffffe',
                          'fileName': '[Nimble_VVOL]rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1.vmdk',
                          'thinProvisioned': True,
                          'datastore': {
                            '_type': 'Datastore',
                            'value': 'datastore-7284'
                          },
                          'backingObjectId': 'rfc4122.2b7d9df3-e668-47b6-964b-7fdad2da737b',
                          'digestEnabled': False
                        },
                        'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                        'diskMode': 'persistent',
                        'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
                        'deltaDiskFormat': 'nativeFormat',
                        'fileName': '[Nimble_VVOL]rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000001.vmdk',
                        'thinProvisioned': True,
                        'datastore': {
                          '_type': 'Datastore',
                          'value': 'datastore-7284'
                        },
                        'backingObjectId': 'rfc4122.83e2dd1e-c29b-435e-b0f3-dd0597cc9cf9',
                        'digestEnabled': False
                      },
                      'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                      'diskMode': 'persistent',
                      'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
                      'deltaDiskFormat': 'nativeFormat',
                      'fileName': '[Nimble_VVOL]rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000002.vmdk',
                      'thinProvisioned': True,
                      'datastore': {
                        '_type': 'Datastore',
                        'value': 'datastore-7284'
                      },
                      'backingObjectId': 'rfc4122.22019129-d231-4157-909d-c149d85e436a',
                      'digestEnabled': False
                    },
                    'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                    'diskMode': 'persistent',
                    'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
                    'deltaDiskFormat': 'nativeFormat',
                    'fileName': "",
                    'thinProvisioned': True,
                    'datastore': {
                      '_type': 'Datastore',
                      'value': 'datastore-7284'
                    },
                    'backingObjectId': 'rfc4122.d1479bff-680c-4ee3-a5fd-c34bbc3c726e',
                    'digestEnabled': False
                  },
                  'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                  'diskMode': 'persistent',
                  'contentId':'a1cf528f9b287bf902f29c42fffffffe',
                  'deltaDiskFormat': 'nativeFormat',
                  'fileName': "",
                  'thinProvisioned': True,
                  'datastore': {
                    '_type': 'Datastore',
                    'value': 'datastore-7284'
                  },
                  'backingObjectId': 'rfc4122.7b8d86b0-0f27-4c47-b7a8-e310980b08f8',
                  'digestEnabled': False
                },
                'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                'diskMode': 'persistent',
                'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
                'deltaDiskFormat': 'nativeFormat',
                'fileName': '',
                'thinProvisioned': True,
                'datastore': {
                  '_type': 'Datastore',
                  'value': 'datastore-7284'
                },
                'backingObjectId': 'rfc4122.23d976b9-7915-41e5-8529-76e963a53665',
                'digestEnabled': False
              },
              'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
              'diskMode': 'persistent',
              'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
              'deltaDiskFormat': 'nativeFormat',
              'fileName': "",
              'thinProvisioned': True,
              'datastore': {
                '_type': 'Datastore',
                'value': 'datastore-7284'
              },
              'backingObjectId': 'rfc4122.0ad747c4-4691-4f29-8b0d-683815b7008a',
              'digestEnabled': False
            },
            'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
            'diskMode': 'persistent',
            'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
            'deltaDiskFormat': 'nativeFormat',
            'fileName': '',
            'thinProvisioned': True,
            'datastore': {
              '_type': 'Datastore',
              'value': 'datastore-7284'
            },
            'backingObjectId': 'rfc4122.ab4f1808-2ee2-4da4-9da6-e7115be9b289',
            'digestEnabled': False
          },
          'sharing': 'sharingNone',
          'uuid': '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
          'diskMode': 'persistent',
          'contentId': 'a1cf528f9b287bf902f29c42fffffffe',
          'deltaDiskFormat': 'nativeFormat',
          'fileName': '',
          'writeThrough': False,
          'split': False,
          'thinProvisioned': True,
          'datastore': {
            '_type': 'Datastore',
            'value': 'datastore-7284'
          },
          'backingObjectId': 'rfc4122.8cd77e1f-153f-41e1-aa9d-860a58f35763',
          'digestEnabled': False
        },
        'diskObjectId': 187-2000,
        'deviceInfo': {
          'label': 'Harddisk1',
          'summary': '2,097,152KB'
        },
        'shares': {
          'shares': 1000,
          'level': 'normal'
        },
        'controllerKey': 1000,
        'unitNumber': 0,
        'capacityInBytes': '2147483648L',
        'key': 2000,
        'storageIOAllocation': {
          'reservation': 0,
          'limit': '-1L',
          'shares': {
            'shares': 1000,
            'level': 'normal'
          }
        },
        'capacityInKB': '2097152L',
        'nativeUnmanagedLinkedClone': False
      }
    }

    parsed_dict = recursive_asdict(d)
    print (parsed_dict)
