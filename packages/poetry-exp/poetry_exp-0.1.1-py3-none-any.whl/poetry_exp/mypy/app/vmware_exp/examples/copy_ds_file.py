#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def copy_file(datacenter_name, source_file_path, destination_file_path):
        datacenter = vcenter_utils.lookup_object(vim.Datacenter, datacenter_name)
        print(datacenter)
        if not datacenter:
            print("Could not find the datastore specified")
            raise SystemExit(-1)

        si = vcenter_utils.connect_vcenter()
        file_manager = si.content.fileManager
        print(f'file_manager: {file_manager}')

        task = file_manager.CopyDatastoreFile_Task(
            source_file_path, datacenter, destination_file_path, datacenter)
        vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    datacenter = "Datacenter1"
    source_file_path = "[NIMBLE_VOL_DS1_15_GB-2021-03-22-05:17:52] abc_vm1/abc_vm1.vmdk"
    destination_file_path = "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1.vmdk"
    copy_file(datacenter, source_file_path, destination_file_path)