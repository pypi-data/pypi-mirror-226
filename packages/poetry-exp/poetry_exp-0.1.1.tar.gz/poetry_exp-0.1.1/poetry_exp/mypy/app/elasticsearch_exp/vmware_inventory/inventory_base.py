import time
from elasticsearch_exp.vmware_inventory import es_utils
from elasticsearch_exp.vmware_inventory import es_const
from elasticsearch_exp.vmware_inventory import constants


class VMWareInventoryBase:
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
        # Maps of newly Added or modified object's moref with document id
        self.cached_hypervisor_hosts_info = dict()
        self.cached_datastores_info = dict()
        self.cached_folders_info = dict()

        self.index_obj_info_map = {
            es_const.INDEX_HYPERVISOR_HOSTS:
                self.cached_hypervisor_hosts_info,
            es_const.INDEX_DATASTORES: self.cached_datastores_info,
            es_const.INDEX_FOLDERS: self.cached_folders_info
        }
        self.vm_ds_map = dict()
        self.ds_hypervisor_hosts_map = dict()

        # Since a VM can part of multiple datastores
        # to avoid processing of vm's vmdks twice
        self.processed_vm_disks = dict()

    def _get_resource_details(self, resource, moref, instance_uuid=None):
        query_params = {
            es_const.HYPERVISOR_MANAGER_INFO + ".id.keyword":
                [self.vcenter_info['id']],
            "moref.keyword": [moref],
        }
        if instance_uuid:
            query_params.update({"instanceUuid.keyword": instance_uuid})
        query = es_utils.create_multiple_terms_query(query_params)
        return es_utils.get_by_query(resource, query)

    def _get_object_info(self, index_name, object_moref):
        """
        Get elastic search doc info corresponding to vim object
        :param index_name: Name of elastic search index
        :param object_details: A dict containing name and moref
        :return: A dict containing doc id and name
        """
        # First check in cached objects
        obj_info = self.index_obj_info_map[index_name].get(object_moref)
        if not obj_info:
            es_obj_details = self._get_resource_details(
                index_name, object_moref)
            if es_obj_details:
                obj_info = {
                    'id': es_obj_details[0]['_id'],
                    'name': es_obj_details[0]['_source']['name']
                }

        if obj_info is None and index_name == es_const.INDEX_FOLDERS:
            obj_info = constants.VMWARE_ROOT_FOLDER_INFO

        return obj_info

    def _add_hypervisor_host(self, host_properties, datacenter_info, cluster_info):
        hypervisor_host_id = es_utils.generate_new_doc_id()
        hypervisor_host_info = {
            'id': hypervisor_host_id,
            'name': host_properties['name']
        }
        host_properties.update({
            'id': hypervisor_host_id,
            es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info,
            es_const.DATACENTER_INFO: datacenter_info,
            es_const.CLUSTER_INFO: cluster_info
        })

        self._add_document(
            es_const.INDEX_HYPERVISOR_HOSTS,
            hypervisor_host_id,
            host_properties
        )
        self.cached_hypervisor_hosts_info[host_properties['moref']] = \
            hypervisor_host_info
        return hypervisor_host_info

    def _add_datastore(self, ds_properties, datacenter_info, cluster_info,
                       hypervisor_hosts_info, folder_info):

        ds_id = es_utils.generate_new_doc_id()
        moref = ds_properties['moref']
        ds_info = {
            'id': ds_id,
            'name': ds_properties['name']
        }

        ds_properties.update({
            'id': ds_id,
            es_const.DATACENTER_INFO: datacenter_info,
            es_const.CLUSTER_INFO: cluster_info,
            es_const.HYPERVISOR_HOSTS_INFO: hypervisor_hosts_info,
            es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info,
            es_const.FOLDER_INFO: folder_info
        })

        self._add_document(
            es_const.INDEX_DATASTORES,
            ds_id,
            ds_properties
        )
        self.cached_datastores_info[moref] = ds_info
        self.ds_hypervisor_hosts_map[moref] = {
            es_const.HYPERVISOR_HOSTS_INFO: hypervisor_hosts_info,
            'id': ds_id
        }
        return ds_info

    def _add_vm(self, vm_properties, datacenter_info, cluster_info,
                hypervisor_host_info, ds_info, folder_info):
        vm_id = es_utils.generate_new_doc_id()
        vm_info = {
            'id': vm_id,
            'name': vm_properties['name']
        }

        vmdks = vm_properties.pop('vmdks')
        vm_properties.update({
            'id': vm_id,
            es_const.HYPERVISOR_MANAGER_INFO: self.vcenter_info,
            es_const.DATACENTER_INFO: datacenter_info,
            es_const.CLUSTER_INFO: cluster_info,
            es_const.HYPERVISOR_HOST_INFO: hypervisor_host_info,
            es_const.DATASTORES_INFO: [ds_info],
            es_const.FOLDER_INFO: folder_info
        })

        self._add_document(
            es_const.INDEX_VIRTUAL_MACHINES,
            vm_id,
            vm_properties
        )
        self.vm_ds_map[vm_properties['moref']] = {
            es_const.DATASTORES_INFO: [ds_info],
            'id': vm_id
        }

        self._add_vmdks(vmdks, vm_properties['moref'], vm_info)
        return vm_info

    def _add_vmdks(self, vmdks, vm_moref, vm_info):
        if not self.processed_vm_disks.get(vm_moref):
            for vmdk in vmdks:
                ds_moref = vmdk.pop('datastore')
                ds_info = self._get_object_info(
                    es_const.INDEX_DATASTORES, ds_moref)
                self._add_vmdk(vmdk, ds_info, vm_info)
            self.processed_vm_disks[vm_moref] = True

    def _add_vmdk(self, vmdk, ds_info, vm_info):
        vmdk_id = es_utils.generate_new_doc_id()
        vmdk.update({
            'id': vmdk_id,
            es_const.DATASTORE_INFO: ds_info,
            es_const.VIRTUAL_MACHINE_INFO: vm_info
        })
        self._add_document(
            es_const.INDEX_VIRTUAL_DISKS,
            vmdk_id,
            vmdk
        )

    def _add_document(self, index_name, doc_id,  doc):
        self.bulk_docs.append({
            es_const.RESOURCE: index_name,
            es_const.ID: doc_id,
            es_const.OPERATION: es_const.INDEX,
            es_const.DOC: doc
        })

    def _update_document(self, index_name, doc_id,  properties_to_update, retry=True):
        args = None
        if retry:
            args = {
                es_const.RETRY_ON_CONFLICT:
                    es_const.RETRY_ATTEMPT_ON_CONFLICT
            }

        self.bulk_docs.append({
            es_const.RESOURCE: index_name,
            es_const.ID: doc_id,
            es_const.OPERATION: es_const.UPDATE,
            es_const.DOC: properties_to_update,
            'args': args
        })

    def _delete_document(self, index_name, doc_id):
        self.bulk_docs.append({
            es_const.RESOURCE: index_name,
            es_const.ID: doc_id,
            es_const.OPERATION: es_const.DELETE
        })

    def _update_bulk_docs(self):
        t1 = time.time()
        #es_utils.update_bulk_docs(self.bulk_docs)
        es_utils.bulk_update(self.bulk_docs)
        t2 = time.time()
        print('Time took to process and update inventory change with ES is'
              ' {0} sec'.format(t2 - t1))
