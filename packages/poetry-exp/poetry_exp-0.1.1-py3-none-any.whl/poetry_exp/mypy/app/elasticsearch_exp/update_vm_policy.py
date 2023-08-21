from elasticsearch_exp import es_crud
import time


def create_vms():
    vm = {
        "id": "1",
        "name": "vm1",
        "moref": "vm-1",
        "uuid": "vmuuid1",
        "datastore": "ds-1",
        "policy": {
            "id": "p1",
            "name": "p1",
            "type": "daily"
        }
    }
    es_crud.insert_doc(vm, "poc-vms")
    vm = {
        "id": "2",
        "name": "vm2",
        "moref": "vm-2",
        "uuid": "vmuuid2",
        "datastore": "ds-2",
        "policy": {
            "id": "p2",
            "name": "p2",
            "type": "monthly"
        }
    }
    es_crud.insert_doc(vm, "poc-vms")


def _update_vm_policy(doc_id, attr_dict_to_update):
    print("Updating VM policy details: {0}".format(attr_dict_to_update))
    time.sleep(5)
    es_crud.update_document_partially(doc_id, attr_dict_to_update, "poc-vms", conflict_retries=3)
    print("VM policy details updated successfully")


def _bulk_update():
    print("Updating docs")
    doc_list = [
        {"id": "1", "policy": {"id": "p1", "name": "P1", "type": "Daily"}},
        {"id": "2", "policy": {"id": "p2", "name": "P2", "type": "Weekly"}}
    ]
    es_crud.bulk_update(doc_list, "poc-vms", conflict_retries=3)
    print("Documents updated successfully")


if __name__ == '__main__':
    policy1 = {"policy": {"id": "p1", "name": "P1", "type": "Daily"}}
    policy2 = {"policy": {"id": "p2", "name": "P2", "type": "Weekly"}}
    policy3 = {"policy": {"id": "p3", "name": "P3", "type": "Monthly"}}
    policy4 = {"policy": {"id": "p4", "name": "P4", "type": "Yearly"}}

    _update_vm_policy("1", policy3)
    # _bulk_update()
