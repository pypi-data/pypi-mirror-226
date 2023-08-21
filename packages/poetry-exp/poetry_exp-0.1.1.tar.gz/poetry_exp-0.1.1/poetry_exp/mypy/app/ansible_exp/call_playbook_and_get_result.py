# -*- coding: utf-8 -*-
import json
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.module_utils.common.collections import ImmutableDict
from ansible import context


extra_vars = {
    "vcenter_hostname": "172.17.29.162",
    "vcenter_username": "administrator@vsphere.local",
    "vcenter_password": "12rmc*Help"
}

context.CLIARGS = ImmutableDict(
    tags={}, extra_vars=[extra_vars], listtags=False, listtasks=False, listhosts=False,
    syntax=False, connection='ssh', module_path=None, forks=100, remote_user='xxx',
    private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
    scp_extra_args=None, become=False, become_method='sudo', become_user='root', verbosity=True,
    check=False, start_at_task=None
)


loader = DataLoader()
variable_manager = VariableManager(loader=loader)
inventory = InventoryManager(loader=loader, sources='localhost,')
variable_manager.set_inventory(inventory)


#get result output
class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = []
        self.host_unreachable = []
        self.host_failed = []

    def v2_runner_on_unreachable(self, result, ignore_errors=False):
        name = result._host.get_name()
        task = result._task.get_name()
        print(result)
        #self.host_unreachable[result._host.get_name()] = result
        self.host_unreachable.append(dict(ip=name, task=task, result=result))

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        name = result._host.get_name()
        task = result._task.get_name()
        if task == "setup":
            pass
        elif "Info" in task:
            self.host_ok.append(dict(ip=name, task=task, result=result))
        else:
            print(result)
            self.host_ok.append(dict(ip=name, task=task, result=result))

    def v2_runner_on_failed(self, result,   *args, **kwargs):
        name = result._host.get_name()
        task = result._task.get_name()
        print(result)
        self.host_failed.append(dict(ip=name, task=task, result=result))

class Options(object):
    def __init__(self):
        self.connection = "smart"
        self.forks = 10
        self.check = False
        self.become = None
        self.become_method = None
        self.become_user=None
    def __getattr__(self, name):
        return None

options = Options()


def run_adhoc(ip,order):
    variable_manager.extra_vars={"ansible_ssh_user":"root" , "ansible_ssh_pass":"passwd"}
    play_source = {"name":"Ansible Ad-Hoc","hosts":"%s"%ip,"gather_facts":"no","tasks":[{"action":{"module":"command","args":"%s"%order}}]}
#    play_source = {"name":"Ansible Ad-Hoc","hosts":"192.168.2.160","gather_facts":"no","tasks":[{"action":{"module":"command","args":"python ~/store.py del"}}]}
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    callback = ResultsCollector()

    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=None,
            run_tree=False,
        )
        tqm._stdout_callback = callback
        result = tqm.run(play)
        return callback

    finally:
        if tqm is not None:
            tqm.cleanup()


def run_playbook(books):
    playbooks = [books]

    #variable_manager.extra_vars={"ansible_ssh_user":"root" , "ansible_ssh_pass":"passwd"}
    callback = ResultsCollector()

    pd = PlaybookExecutor(
        playbooks=playbooks,
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        #options=options,
        passwords=None,

        )
    pd._tqm._stdout_callback = callback

    try:
        result = pd.run()
        return callback

    except Exception as e:
        print (e)

if __name__ == '__main__':
    result = run_playbook("get_vms.yml")
    print(result)
    print(result.host_ok)
    for host in result.host_ok:
        #print(dir(host['result']))
        print( host['result']._result)
        #print(json.dumps({host.name: host['result']._result}, indent=4))

    #run_adhoc("192.168.2.149", "ifconfig")