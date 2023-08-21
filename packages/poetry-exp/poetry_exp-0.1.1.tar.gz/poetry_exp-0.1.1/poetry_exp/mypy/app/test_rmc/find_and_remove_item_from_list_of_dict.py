protected_resource = {
  "datastores": [
    {
      "name": "DS-Mumbai-Dev1",
      "vmwareId": "datastore-264"
    },
    {
      "name": "DS-Banglore-Dev2",
      "vmwareId": "datastore-2555"
    },
    {
      "name": "DS-Bangalore-Dev1",
      "vmwareId": "datastore-219"
    }
  ],
  "virtualmachines": [
    {
      "name": "A1 New Virtual Machine",
      "vmwareId": "vm-6178"
    },
    {
      "name": "VM-Bangalore-Dev3-Partial1",
      "vmwareId": "vm-2658"
    },
    {
      "name": "VM-Bangalore-Dev3",
      "vmwareId": "vm-2591"
    },
    {
      "name": "New Virtual Machine2",
      "vmwareId": "vm-6177"
    },
    {
      "name": "VM-Bangalore-Dev4",
      "vmwareId": "vm-2999"
    },
    {
      "name": "VM-Bangalore-Dev1",
      "vmwareId": "vm-544"
    }
  ]
}


def add_resources_to_protected_resources(protected_ds, protected_vm, existing_protected_resources):
    existing_datastores = existing_protected_resources.get("datastores", [])
    existing_vms = existing_protected_resources.get("virtualmachines", [])
    for datastore in protected_ds:
        if not datastore["vmwareId"] in [ds["vmwareId"] for ds in existing_datastores]:
            existing_datastores.append(datastore)
    for vm in protected_vm:
        if not vm["vmwareId"] in [v["vmwareId"] for v in existing_vms]:
            existing_vms.append(vm)


def delete_resource_from_protected_resources(morefs_to_be_deleted, existing_protected_resources):
    datastores = existing_protected_resources.get("datastores", [])
    vms = existing_protected_resources.get("virtualmachines", [])
    for moref in morefs_to_be_deleted:
        for datastore in datastores:
            if moref == datastore["vmwareId"]:
                datastores.remove(datastore)
        for vm in vms:
            if moref == vm["vmwareId"]:
                vms.remove(vm)

if __name__ == '__main__':
    morefs_to_be_deleted = ['vm-2591', 'datastore-2555']
    #delete_resource_from_protected_resources(morefs_to_be_deleted, protected_resource)
    #print(protected_resource)
    ds = [{"vmwareId": 'datastore-111111', 'name': 'DS1111111'},{"vmwareId": 'datastore-2555', 'name': 'DS-Banglore-Dev2'}, {"vmwareId": 'datastore-22222', 'name': 'DS22222'}]
    vms = [{"vmwareId": 'vm-333333', 'name': 'VM333333'},{"vmwareId": 'vm-2591', 'name': 'VM-Bangalore-Dev3'}, {"vmwareId": 'vm-444444', 'name': 'VM4444444'}]
    add_resources_to_protected_resources(ds, vms, protected_resource)
    print(protected_resource)