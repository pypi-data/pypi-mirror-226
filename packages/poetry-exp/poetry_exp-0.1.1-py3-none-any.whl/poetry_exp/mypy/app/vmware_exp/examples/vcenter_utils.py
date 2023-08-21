from pyVim import connect
from pyVmomi import vim
from conf import constants
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ssl_context.verify_mode = ssl.CERT_NONE
#
HOST = "172.17.29.162" #constants.VCENTER_HOST
USER = "administrator@vsphere.local" #constants.VCENTER_USER
PASSWORD = "12iso*Help" #constants.VCENTER_PASSWORD
PORT = 443 #constants.VCENTER_PORT

#
# HOST = "15.252.220.58" #constants.VCENTER_HOST
# USER = "administrator@vsphere.local" #constants.VCENTER_USER
# PASSWORD = "Admin!23" #constants.VCENTER_PASSWORD
# PORT = 443 #constants.VCENTER_PORT

#
# HOST = "172.17.29.235" #constants.VCENTER_HOST
# USER = "administrator@vsphere.local" #constants.VCENTER_USER
# PASSWORD = "12iso*Help" #constants.VCENTER_PASSWORD
# PORT = 443 #constants.VCENTER_PORT

def connect_vcenter(host=HOST, username=USER, password=PASSWORD, port=PORT):
    print('connecting to vcenter...')
    service_instance = connect.SmartConnect(host=host,
                                            user=username,
                                            pwd=password,
                                            port=port,
                                            sslContext=ssl_context)
    print ('connected, vcenter: %s', service_instance)
    return service_instance


def list_datacenter():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.Datacenter], True)
    datacenters = container.view
    for datacenter in datacenters:
        print (datacenter.name)
    return datacenters

def list_datastore():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.Datastore], True)
    datastores = container.view
    for datastore in datastores:
        print (datastore.name)


def list_cluster():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.ClusterComputeResource], True)
    clusters = container.view
    for cluster in clusters:
        print(cluster.name)
        print(cluster._moId) # domain-c28673

    return clusters


def list_resource_pool():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.ResourcePool], True)
    resource_pools = container.view
    for pool in resource_pools:
        print (pool.name)
    return resource_pools


def list_host():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.HostSystem], True)
    hosts = container.view
    for host in hosts:
       print (host.name)
    return hosts


def list_host_cluster_by_cluster():
    hosts = list()
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.ComputeResource], True)
    clusters = container.view
    for cluster in clusters:
        print ('Hosts in cluster: %s', cluster.name)
        for host in cluster.host:
            print (host.name)
            hosts.append(host)
    return hosts


def list_vm():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    for vm in vms:
        print (dir(vm))
        break

    return vms


def lookup_object(vimtype, name):
    """Look up an object by name.

    Args:
      vimtype (object): currently only ``vim.VirtualMachine``
      name (str): Name of the object to look up.
    Returns:
      object: Located object
    """
    si = connect_vcenter()
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], True)
    for item in container.view:
        if item.name == name:
            return item
    return None


def lookup_object_by_moref(vimtype, moref_id):
    """Look up an object by name.

    Args:
      vimtype (object): currently only ``vim.VirtualMachine``
      name (str): Name of the object to look up.
    Returns:
      object: Located object
    """
    si = connect_vcenter()
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], True)
    for item in container.view:
        if item._moId == moref_id:
            return item
    return None


def get_moref(obj_type, moref_id):
    method = getattr(vim, obj_type)
    mob_ref = method(moref_id)
    return mob_ref


def get_object_by_moref(obj_type, moref, obj_props, get_all_props=False, traversal_spec_list=None):
    si = connect_vcenter()
    service_content = si.RetrieveContent()

    method = getattr(vim, obj_type)
    mob_ref = method(moref)

    mo_type = getattr(vim, obj_type)

    property_spec = vim.PropertyCollector.PropertySpec(
        all=get_all_props, pathSet=obj_props, type=mo_type)

    obj_spec = vim.PropertyCollector.ObjectSpec(
        obj=mob_ref, selectSet=traversal_spec_list, skip=False)

    prop_filter_spec = vim.PropertyCollector.FilterSpec(
        objectSet=[obj_spec], propSet=[property_spec],
        reportMissingObjectsInResults=False)
    ret_options = vim.PropertyCollector.RetrieveOptions()
    total_props = []
    ret_props = service_content.propertyCollector.RetrievePropertiesEx(
        specSet=[prop_filter_spec], options=ret_options)

    if ret_props:
        total_props += ret_props.objects
        while ret_props.token:
            ret_props = service_content.propertyCollector. \
                ContinueRetrievePropertiesEx(token=ret_props.token)
            total_props += ret_props.objects
    object_contents = total_props
    prop_dict = {}

    for oc in object_contents:
        properties = oc.propSet
        if properties:
            for each_prop in properties:
                prop_dict[each_prop.name] = each_prop.val
    return prop_dict


def list_network():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.Network], True)
    networks = container.view
    for network in networks:
        print (network.name)


def list_event():
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    event_manager = vcenter_content.eventManager
    event_filter_spec = vim.event.EventFilterSpec()
    event_res = event_manager.QueryEvents(event_filter_spec)
    for e in event_res:
        print("{} \033[32m@\033[0m {:%Y-%m-%d %H:%M:%S}".format(
            e.fullFormattedMessage, e.createdTime))


def list_vm_event(vm_name='ubuntu-clone'):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    for vm in vms:
        #print (vm.name)
        if vm.name == vm_name:
            event_manager = vcenter_content.eventManager
            event_filter_spec = vim.event.EventFilterSpec()
            filter = vim.event.EventFilterSpec.ByEntity(
                entity=vm, recursion="self")
            event_filter_spec.entity = filter

            event_res = event_manager.QueryEvents(event_filter_spec)
            for e in event_res:
                print(e.__dict__)
                print("{} \033[32m@\033[0m {:%Y-%m-%d %H:%M:%S}".format(
                    e.fullFormattedMessage, e.createdTime))



def list_snapshot(vm_name='vrb'):
    si = connect_vcenter()
    vcenter_content = si.RetrieveContent()
    inventory_path = '{0}/vm/{1}'.format(constants.VCENTER_DATACENTER, vm_name)
    vm = vcenter_content.searchIndex.FindByInventoryPath(inventory_path)
    if vm:
        print ('Found the VM')
        snap_info = vm.snapshot
        print (snap_info)
        snap_tree = snap_info.rootSnapshotList
        while snap_tree[0].childSnapshotList is not None:
            print("Snap: {0} => {1}".format(snap_tree[0].name, snap_tree[0].description))
            if len(snap_tree[0].childSnapshotList) < 1:
                break
            snap_tree = snap_tree[0].childSnapshotList

    else:
        raise Exception('Cannot find the VM {}'.format(vm_name))


def list_dvswitch():
    dvs_list = list()
    si = connect_vcenter()
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.dvs.VmwareDistributedVirtualSwitch], True)
    dvswitches = container.view

    for dvswitch in dvswitches:
        print (dvswitch.name)
        dvs_list.append(dvswitch)

    return dvs_list


def get_dvswitch_name(dvs_name):
    dvs_list = list_dvswitch()
    for dvs in dvs_list:
        if dvs.name == dvs_name:
            return dvs


def list_port_group():
    portgroups = list()
    dvswitches = list_dvswitch()
    for dvswitch in dvswitches:
        for portgroup in dvswitch.portgroup:
            print (portgroup.name)
            portgroups.append(portgroup)

    return portgroups


def wait_for_task(task, return_task=False):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print (f'Task done, result: {task.info.result}')
            if return_task:
                return task
            return task.info.result
        if task.info.state == 'error':
            print (f'Task failed: error: {task.info.error.msg}')
            task_done = True
            if return_task:
                return task
            return task.info.error.msg


def get_port_group_config_spec(port_group_name):
    config = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
    config.name = port_group_name
    config.type = constants.PORT_GROUP_TYPE
    config.numPorts = constants.NUM_OF_PORT

    config.defaultPortConfig  = vim.VMwareDVSPortSetting()
    config.defaultPortConfig.vlan = vim.VmwareDistributedVirtualSwitchVlanIdSpec()
    config.defaultPortConfig.vlan.inherited = False
    config.defaultPortConfig.vlan.vlanId = constants.VLAN_ID

    config.defaultPortConfig.uplinkTeamingPolicy = vim.dvs.VmwareDistributedVirtualSwitch.UplinkPortTeamingPolicy()
    config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder = \
        vim.dvs.VmwareDistributedVirtualSwitch.UplinkPortOrderPolicy()
    config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.activeUplinkPort = constants.ACTIVE_LINK_NAME
    config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.standbyUplinkPort = constants.STANDBY_LINK_NAME
    return config


def create_port_group(port_group_name):
    si = connect_vcenter()
    print ('Creating port group....')
    dvs = get_dvswitch_name(constants.DIST_VIRTUAL_SWITCH_NAME)
    if dvs is None:
        raise Exception('dvSwitch not found with name {0}'.format(
            constants.DIST_VIRTUAL_SWITCH_NAME))

    port_group_conf_spec = get_port_group_config_spec(port_group_name)
    task = dvs.AddDVPortgroup_Task([port_group_conf_spec])
    result = wait_for_task(task)
    print (result)


if __name__== '__main__':
    #list_cluster()
    # connect_vcenter()
    # list_datastore()
    # list_resource_pool()
    # list_datacenter()
    # list_host()
    # list_host_cluster_by_cluster()
    #list_vm()
    # list_network()
    # list_event()
    list_vm_event()
    # list_snapshot()
    # list_dvswitch()
    # list_port_group()
    #create_port_group('Autmation_test')