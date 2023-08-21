from conf import constants
import vcenter_utils
from pyVmomi import vim

TEMPLATE_NAME = 'ehc-win-template'



def get_vcenter_obj(vim_type, obj_name):
    service_instance = vcenter_utils.connect_vcenter()
    vcenter_content = service_instance.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, vim_type, True)
    vcenter_objects = container.view
    for obj in vcenter_objects:
        print (obj)
        if obj.name == obj_name:
            print ('Found the object: ', obj_name)
            return obj
            break


def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print ('Task done')
            return task.info.result
        if task.info.state == 'error':
            print ('Task failed')
            task_done = True
            return task.info



def create_clone(vm_or_template_name, vm_name):
    #vm_name or template name
    template = get_vcenter_obj([vim.VirtualMachine], vm_or_template_name)
    print (template)
    dest_folder = get_vcenter_obj(
        [vim.Datacenter], constants.VCENTER_DATACENTER)

    relocate_spec = vim.vm.RelocateSpec()

    clone_spec = vim.vm.CloneSpec()
    clone_spec.location = relocate_spec

    task = template.Clone(
        folder = dest_folder.vmFolder, name=vm_name, spec=clone_spec)
    result = wait_for_task(task)
    print (result)

def create_clone2(vm_or_template_name, vm_name,
                  vm_folder=None, datastore_name=None,
                  resource_pool_name=None):
    template = get_vcenter_obj([vim.VirtualMachine], vm_or_template_name)

    data_center = get_vcenter_obj([vim.Datacenter], constants.VCENTER_DATACENTER)
    if vm_folder:
        dest_folder = get_vcenter_obj([vim.Folder], vm_folder)
    else:
        dest_folder = data_center.vmFolder

    if datastore_name:
        datastore = get_vcenter_obj([vim.Datastore], datastore_name)
    else:
        datastore = get_vcenter_obj([vim.Datastore], template.datastore[0].info.name)

    cluster = get_vcenter_obj([vim.ClusterComputeResource], constants.VCENTER_CLUSTER)

    if resource_pool_name:
        resource_pool = get_vcenter_obj([vim.ResourcePool], resource_pool_name)
    else:
        resource_pool = cluster.resourcePool

    relocate_spec = vim.vm.RelocateSpec()
    relocate_spec.datastore = datastore
    relocate_spec.pool = resource_pool

    clone_spec = vim.vm.CloneSpec()
    clone_spec.location = relocate_spec

    task = template.Clone(folder=dest_folder, name=vm_name, spec=clone_spec)
    result = wait_for_task(task)
    print (result)





'''
Received message {'method_name': 'deployAutomationPodVM', 'module_name': 'common.vCenterOps',
 'method_params': {'guestCustomization': {'vmCustomSpecInfoName': 'spec-ehc-windows-test-vm-20170731043825',
  'userFullName': 'administrator', 'vmCustomSpecInfoType': 'Windows', 'domainAdminPassword': '*********',
   'vmIPSubnetMask': '255.255.252.0', 'domainAdmin': 'administrator', 'vmTimeZone': '035', 'computerName': 'sql01',
    'joinDomain': 'pod6.local', 'vmLicenseAutoMode': 'perServer',
     'windowsProductKey': 'YKCCP-HYNQC-HMJ8Q-9G37R-8422W', 'vmIPDNSServerList': '192.168.194.106',
      'vmAutoLogonCount': 1, 'administratorPassword': '*********', 'vmLicenseAutoUsers': 5,
       'vmAutoLogon': True, 'userOrgName': 'EHC', 'vmIPFixedIPAddress': '192.168.194.20',
        'vmCustomSpecInfoDescription': 'Description', 'vmIPGateway': '192.168.192.1'},
         'vCenterDataDict': {'port': 443, 'vCenterIPAddress': '192.168.133.164',
          'vCenterUsername': 'administrator@vsphere.local', 'vCenterPassword': '*********'},
           'timeout': 3600, 'vmDetails': [{'resourcePool': 'Automation', 'clusterName': 'Clean_Compute',
            'dataStoreName': 'pod6', 'vmMemoryConfig': {'memorySize': '4'}, 'dataCenterName': 'Datacenter',
             'cpuConfig': {'numCPUs': '2', 'numCoresPerSocket': '2'}, 'powerON': True,
              'vmName': 'ehc-windows-test-vm'}],
               'templateName': 'ehc-win-template'}
               , 'unique_id': 'bd893c46-c597-4d08-8c3c-63ddeef257bd', 'no_log': 'False'}  

'''

if __name__=='__main__':
    #create_clone(TEMPLATE_NAME, 'test_vm')
    #create_clone('test_vm', 'test_clone_by_vm')
    #create_clone2(TEMPLATE_NAME, 'test_vm3')
    create_clone2(TEMPLATE_NAME, 'test_vm4',
                  vm_folder=constants.VCENTER_VM_FOLDER,
                  datastore_name=constants.VCENTER_DATASTORE,
                  resource_pool_name=constants.VCENTER_RESOURCE_POOL)
