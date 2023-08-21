#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def relocate_vm(vm_name, target_ds_name):
        vm = vcenter_utils.lookup_object(vim.VirtualMachine, vm_name)
        ds = vcenter_utils.lookup_object(vim.Datastore, target_ds_name)
        spec = vim.vm.RelocateSpec()
        spec.datastore = ds
        si = vcenter_utils.connect_vcenter()
        prov_checker = si.content.vmProvisioningChecker
        task = prov_checker.CheckRelocate_Task(vm, spec=spec)
        results = vcenter_utils.wait_for_task(task)

        locate_possible = True
        for result in results:
            if result.error:
                locate_possible = False
                break
        print(f"VM can be relocated: {locate_possible}")

        task = vm.RelocateVM_Task(spec)
        vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    datastore = "NIMBLE_VOL_DS3_17_GB"

    relocate_vm("orig_vm3", datastore)