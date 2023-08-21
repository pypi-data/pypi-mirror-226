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


def _update_vm_properties(doc_id, attr_dict_to_update):
    print("Updating VM properties: {0}".format(attr_dict_to_update))
    time.sleep(7)
    es_crud.update_document_partially(doc_id, attr_dict_to_update, "poc-vms", conflict_retries=3)
    print("VM properties updated successfully")


def _bulk_update():
    print("Updating docs")
    doc_list = [
        {"id": "1", "name": "dev-vm1111", "datastore": "ds-1"},
        {"id": "2", "name": "prod-vm22222", "datastore": "ds-2"}
    ]
    es_crud.bulk_update(doc_list, "poc-vms", conflict_retries=3)
    print("Documents updated successfully")



if __name__ == '__main__':
    #create_vms()
    prop1 = {"name": "dev-vm1", "datastore": "ds-1"}
    prop2 = {"name": "prod-vm2", "datastore": "ds-2"}
    _update_vm_properties("1", prop1)

    # _bulk_update()



"""
GET /poc-vms/_doc/1
Response:
{
  "_index" : "poc-vms",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 7,
  "_seq_no" : 7,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "id" : "1",
    "name" : "dev-vm1",
    "moref" : "vm-1",
    "uuid" : "vmuuid1",
    "datastore" : "ds-1",
    "policy" : {
      "id" : "p2",
      "name" : "P2",
      "type" : "Weekly"
    }
  }
}

# Partial update of document
POST /poc-vms/_update/1?retry_on_conflict=5
{
  "doc": {"name": "qa-vm1"}
}

Response:
{
  "_index" : "poc-vms",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 8,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 8,
  "_primary_term" : 1
}


GET /poc-vms/_doc/1
Response:
{
  "_index" : "poc-vms",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 8,
  "_seq_no" : 8,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "id" : "1",
    "name" : "qa-vm1",  # Updated only name
    "moref" : "vm-1",
    "uuid" : "vmuuid1",
    "datastore" : "ds-1",
    "policy" : {
      "id" : "p2",
      "name" : "P2",
      "type" : "Weekly"
    }
  }
}

"""
