#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def copy_vmdk(datacenter_name, source_file_path, destination_file_path, overwrite=False):
        datacenter = vcenter_utils.lookup_object(vim.Datacenter, datacenter_name)
        print(datacenter)
        if not datacenter:
            print("Could not find the datastore specified")
            raise SystemExit(-1)

        si = vcenter_utils.connect_vcenter()
        vmdk_manager = si.content.virtualDiskManager
        print(f'vmdk_manager: {vmdk_manager}')

        task = vmdk_manager.CopyVirtualDisk_Task(
            source_file_path, datacenter, destination_file_path, datacenter, force=overwrite)
        vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    overwrite = True
    # with overwrite False
    # Task failed: error: Cannot complete the operation because the file or folder [NIMBLE-VOL-DS1-15-GB] test_vm4/test_vm4.vmdk already exists
    # with overwrite True
    # Task failed: error: Cannot complete the operation because the file or folder [NIMBLE-VOL-DS1-15-GB] test_vm4/test_vm4.vmdk already exists
    # Same behaviour: This flag is getting ignored
    datacenter = "Datacenter1"
    source_file_path = "[NIMBLE-VOL-DS1-15-GB-2021-04-01-05:47:58] test_vm4/test_vm4.vmdk"
    destination_file_path = "[NIMBLE-VOL-DS1-15-GB] test_vm4/test_vm4_test_attach.vmdk"
    copy_vmdk(datacenter, source_file_path, destination_file_path, overwrite)