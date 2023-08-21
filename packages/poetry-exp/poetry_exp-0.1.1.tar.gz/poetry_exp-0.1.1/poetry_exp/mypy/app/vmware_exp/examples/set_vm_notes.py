import re
import time
from datetime import datetime
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils
import re

# https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/set_note.py
PROTECTION_NOTES_PREFIX = "Protected by HPE BRS with Protection Policy '"
PROTECTION_NOTES_PATTERNS = re.compile(r"Protected by HPE BRS with Protection Policy.*'")

REMOVE_PROTECTION_NOTES_PATTERNS = re.compile(r"Protected by HPE BRS with Protection Policy.*'.*'")


def set_vm_notes(vm, notes=""):
    print('Setting notes....')
    if notes:
        spec = vim.vm.ConfigSpec()
        spec.annotation = notes
        task = vm.ReconfigVM_Task(spec=spec)
        vcenter_utils.wait_for_task(task)
        print(f'Successfully set the notes: {notes}')
    else:
        print('No notes provided')


def get_notes(policy_name):
    return PROTECTION_NOTES_PREFIX + policy_name + "'"


def get_updated_notes(vm, notes, notes_pattern_to_replace=None, remove_notes=False):
    existing_notes = vm.summary.config.annotation
    print(f'existing_notes: {existing_notes}')
    new_notes = notes
    if existing_notes:
        if notes in existing_notes:
            print(f"Given notes: '{notes}' already exists in the existing notes: '{existing_notes}'")
            # if remove_notes:
            #     new_notes = re.sub(notes_pattern_to_replace, "", existing_notes)
            # else:
            return
        elif notes_pattern_to_replace and re.search(notes_pattern_to_replace, existing_notes):
            print("Given note pattern found in existing notes, replacing the notes")
            new_notes = re.sub(notes_pattern_to_replace, notes, existing_notes)
        else:
            print(f'Given notes not found in existing notes, appending the notes')
            new_notes = existing_notes + "\n" + notes
    print(f'new_notes: {new_notes}')
    return new_notes


def set_notes(vm, notes, note_pattern_to_check=None):
    new_notes = get_updated_notes(vm, notes, note_pattern_to_check)
    if new_notes:
        set_vm_notes(vm, new_notes)

if __name__ == '__main__':
    # snapshot = vcenter_utils.lookup_object(vim.Snapshot, virtual_machine_name)

    #virtual_machine_name = 'win2016_cbt_test_vm1'
    #
    # virtual_machine_name = 'primra_small_vm1_edit'
    # vm = vcenter_utils.lookup_object(vim.VirtualMachine, virtual_machine_name)
    # print(f'VM: {vm}')
    # set_notes(vm, get_notes("p6"), PROTECTION_NOTES_PATTERNS)
    # #set_notes(vm, 'get_notes("p4")')


    existing_notes = "Protected by HPE BRS with Protection Policy 'p1'\n TEst12345"
    # found_pattern = re.search(PROTECTION_NOTES_PATTERNS, existing_notes)
    # print(f'found_pattern: {found_pattern}')
    # new_notes = re.sub(PROTECTION_NOTES_PATTERNS, get_notes("p6"), existing_notes)
    # print(new_notes)

    # Remove notes:
    existing_notes = "TEst111111\nProtected by HPE BRS with Protection Policy 'p1'\n Test2222"
    existing_notes = "Protected by HPE BRS with1 Protection Policy 'p1'"

    remove_notes = PROTECTION_NOTES_PREFIX
    new_notes = None
    if remove_notes in existing_notes:
        new_notes = re.sub(REMOVE_PROTECTION_NOTES_PATTERNS, "", existing_notes)
        new_notes = "\n".join(
            [n for n in new_notes.split("\n") if n])
    print(new_notes)
    if new_notes is None:
        print("No new notes")

