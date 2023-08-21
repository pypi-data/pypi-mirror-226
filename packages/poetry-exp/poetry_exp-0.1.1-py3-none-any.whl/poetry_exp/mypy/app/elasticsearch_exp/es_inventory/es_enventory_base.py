import time
from elasticsearch_exp.es_inventory import es_utils


class ESInventoryBase:
    """
    Base class for inventory build and update
    """
    def __init__(self, vcenter_dict):
        self.vcenter_dict = vcenter_dict
        self.vcenter_info = {
            'id':  self.vcenter_dict['id'],
            'name':  self.vcenter_dict['name']
        }
        self.bulk_docs = []

    def _update_bulk_docs(self):
        t1 = time.time()
        es_utils.update_bulk_docs(self.bulk_docs)
        t2 = time.time()
        print('Time took to process and update inventory change with ES is'
              ' {0} sec'.format(t2 - t1))
