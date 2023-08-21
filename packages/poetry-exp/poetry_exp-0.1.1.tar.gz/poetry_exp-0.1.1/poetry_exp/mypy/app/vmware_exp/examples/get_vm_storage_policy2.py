import re
import time
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils
import re
import ssl

from pyVmomi import pbm, vim, VmomiSupport, SoapStubAdapter



class BColors(object):
    """A class used to represent ANSI escape sequences
       for console color output.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def pbm_connect(stub_adapter, disable_ssl_verification=False):
    """Connect to the VMware Storage Policy Server
    :param stub_adapter: The ServiceInstance stub adapter
    :type stub_adapter: SoapStubAdapter
    :param disable_ssl_verification: A flag used to skip ssl certificate
        verification (default is False)
    :type disable_ssl_verification: bool
    :returns: A VMware Storage Policy Service content object
    :rtype: ServiceContent
    """

    # if disable_ssl_verification:
    #     import ssl
    #     if hasattr(ssl, '_create_unverified_context'):
    #         ssl_context = ssl._create_unverified_context()
    #     else:
    #         ssl_context = None
    # else:
    #     ssl_context = None

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False

    ssl_context.verify_mode = ssl.CERT_NONE
    VmomiSupport.GetRequestContext()["vcSessionCookie"] = \
        stub_adapter.cookie.split('"')[1]
    hostname = stub_adapter.host.split(":")[0]
    pbm_stub = SoapStubAdapter(
        host=hostname,
        version="pbm.version.version1",
        path="/pbm/sdk",
        poolSize=0,
        sslContext=ssl_context)
    pbm_si = pbm.ServiceInstance("ServiceInstance", pbm_stub)
    pbm_content = pbm_si.RetrieveContent()
    return pbm_content


def get_storage_profiles(profile_manager, ref):
    """Get vmware storage policy profiles associated with specified entities
    :param profileManager: A VMware Storage Policy Service manager object
    :type profileManager: pbm.profile.ProfileManager
    :param ref: A server reference to a virtual machine, virtual disk,
        or datastore
    :type ref: pbm.ServerObjectRef
    :returns: A list of VMware Storage Policy profiles associated with
        the specified entities
    :rtype: pbm.profile.Profile[]
    """

    profiles = []
    profile_ids = profile_manager.PbmQueryAssociatedProfile(ref)
    if len(profile_ids) > 0:
        profiles = profile_manager.PbmRetrieveContent(profileIds=profile_ids)
        return profiles
    return profiles


def show_storage_profile_capabilities(capabilities):
    """Print vmware storage policy profile capabilities
    :param capabilities: A list of VMware Storage Policy profile
        associated capabilities
    :type capabilities: pbm.capability.AssociatedPolicyCapabilities
    :returns: None
    """

    for capability in capabilities:
        for constraint in capability.constraint:
            if hasattr(constraint, 'propertyInstance'):
                for propertyInstance in constraint.propertyInstance:
                    print("\tKey: {} Value: {}".format(propertyInstance.id,
                                                       propertyInstance.value))


def show_storage_profile(profiles):
    """Print vmware storage policy profile
    :param profiles: A list of VMware Storage Policy profiles
    :type profiles: pbm.profile.Profile[]
    :returns: None
    """

    for profile in profiles:
        print("Name: {}{}{} ".format(BColors.OKGREEN,
                                     profile.name,
                                     BColors.ENDC))
        print("ID: {} ".format(profile.profileId.uniqueId))
        print("Description: {} ".format(profile.description))
        print("profile: {} ".format(profile))
        print("profile: {} ".format(profile.__dict__))

        if hasattr(profile.constraints, 'subProfiles'):
            subprofiles = profile.constraints.subProfiles
            for subprofile in subprofiles:
                print("RuleSetName: {} ".format(subprofile.name))
                capabilities = subprofile.capability
                show_storage_profile_capabilities(capabilities)


def get_vm_storage_policy(vm_name):
    vm_profiles = []
    si = vcenter_utils.connect_vcenter()
    pbm_content = pbm_connect(si._stub)
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
    pm = pbm_content.profileManager
    pm_object_type = pbm.ServerObjectRef.ObjectType("virtualMachine")
    print(f'....aafak...vm._moId:{vm._moId}')
    pm_ref = pbm.ServerObjectRef(key=vm._moId, objectType=pm_object_type)
    profiles = get_storage_profiles(pm, pm_ref)
    if len(profiles) > 0:
        print("Home Storage Profile:")
        show_storage_profile(profiles)

    print("\r\nVirtual Disk Storage Profile:")
    for device in vm.config.hardware.device:
        device_type = type(device).__name__
        if device_type == "vim.vm.device.VirtualDisk":
            pm_object_type = pbm.ServerObjectRef.ObjectType("virtualDiskId")
            pm_ref = pbm.ServerObjectRef(
                key="{}:{}".format(vm._moId, device.key), objectType=pm_object_type)
            vm_profiles = get_storage_profiles(pm, pm_ref)
            break

    print(f'VM: {vm_name}, profiles: {vm_profiles}')

    for vm_profile in vm_profiles:
        profile_type = vm_profile.resourceType.resourceType
        print(f'profile_type: {vm_profile.resourceType.resourceType}')
        if profile_type == 'STORAGE':
            sub_profiles = getattr(vm_profile.constraints, 'subProfiles', [])
            if not sub_profiles:
                print(f'No sub profiles found')
                return
            for sp in sub_profiles:
                if sp.name == 'HPE Primera rules':
                    capabilities = sp.capability
                    for capability in capabilities:
                        print(capability)
                        if capability.id.namespace == 'com.hpe.primera.spbm.dataprotection':
                            constraints = capability.constraint
                            for constraint in constraints:
                                property_instances = constraint.propertyInstance
                                print(f'property_instances: {property_instances}')
                                for pi in property_instances:
                                    if pi.id == 'dataProtectionPolicy':
                                        print(f'........vm policy: {pi.value}')
                                        return pi.value
    # if len(profiles) > 0:
            #     print(device.deviceInfo.label)
            #     show_storage_profile(profiles)
            #     print("")
    print("")

    print(f'VM: {vm}')


if __name__ == '__main__':
    vm_name = "prim75_vvol_vm1"
    vm_name = "VM1"

    get_vm_storage_policy(vm_name)
