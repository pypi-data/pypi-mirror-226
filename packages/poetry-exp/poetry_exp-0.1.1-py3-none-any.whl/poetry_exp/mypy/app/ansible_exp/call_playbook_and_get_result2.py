# -*- coding: utf-8 -*-
import json
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.module_utils.common.collections import ImmutableDict
from ansible import context

CLI_ARGS = dict(tags={}, listtags=False, listtasks=False, listhosts=False,
    syntax=False, connection='ssh', module_path=None, forks=100, remote_user='xxx',
    private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
    scp_extra_args=None, become=False, become_method='sudo', become_user='root', verbosity=True,
    check=False, start_at_task=None)


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


def run_playbook(playbook_file, playbook_args):
    playbooks = [playbook_file]

    # Setting playbook args
    CLI_ARGS['extra_vars'] = [playbook_args]
    context.CLIARGS = ImmutableDict(CLI_ARGS)

    callback = ResultsCollector()

    loader = DataLoader()
    variable_manager = VariableManager(loader=loader)
    inventory = InventoryManager(loader=loader, sources='localhost,')
    variable_manager.set_inventory(inventory)

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
        if result == 0:
            print('Playbook ran successfully')
            for host in callback.host_ok:
                return host['result']._result
        else:
            print('Eror: Playbook could not run successfully')
            for host in callback.host_failed:
                return host['result']._result

    except Exception as e:
        print(e)


def get_all_vms(vcenter_details):
    return run_playbook("get_vms.yml", vcenter_details)


def get_all_datastores(vcenter_details):
    return run_playbook("get_datastores.yml", vcenter_details)


if __name__ == '__main__':
    vcenter_details = {
        "vcenter_hostname": "172.17.29.162",
        "vcenter_username": "administrator@vsphere.local",
        "vcenter_password": "12rmc*Help",
        "datacenter_name": 'Datacenter1'
    }
    # result = get_all_datastores(vcenter_details)
    # print(result)

    result = get_all_vms(vcenter_details)
    print(result)





"""
output Sample:
aafak@aafak-virtual-machine:~/aafak/ansible_exp$ python3.6 call_playbook_and_get_result2.py
[WARNING]: Unable to parse localhost, as an inventory source
[WARNING]: No inventory was parsed, only implicit localhost is available
<ansible.executor.task_result.TaskResult object at 0x7f0cea82c6d8>
<ansible.executor.task_result.TaskResult object at 0x7f0cea838898>
Playbook ran successfully
{
  'changed': False,
  'datastores': [
    {
      'accessible': False,
      'capacity': 48559973990400,
      'name': '3PAR_VVOL_DS2',
      'freeSpace': 23736136761344,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VVOL',
      'uncommitted': 2335866880,
      'url': 'ds:///vmfs/volumes/vvol:b111450adb064dde-98c4dd14ce7fd02e/',
      'provisioned': 24826173095936,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 10468982784,
      'name': '3PAR_Aafak_New_RCG1',
      'freeSpace': 4664066048,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VMFS',
      'uncommitted': 6849512363,
      'url': 'ds:///vmfs/volumes/5eb25e9f-66fde300-0124-5cb901e28430/',
      'provisioned': 12654429099,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': False,
      'capacity': 48559973990400,
      'name': '3PAR_VVOL_DS1',
      'freeSpace': 23736136761344,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VVOL',
      'uncommitted': 0,
      'url': 'ds:///vmfs/volumes/vvol:f79db2e03c9a475e-931cd7b5e25da837/',
      'provisioned': 24823837229056,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 107105746944,
      'name': 'DS-Washington-Dev1-RC1',
      'freeSpace': 102106136576,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VMFS',
      'uncommitted': 4483350994,
      'url': 'ds:///vmfs/volumes/5cee4962-4068026a-df9d-2c44fd82f008/',
      'provisioned': 9482961362,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 992137445376,
      'name': 'datastore1',
      'freeSpace': 367213412352,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VMFS',
      'uncommitted': 1743433655335,
      'url': 'ds:///vmfs/volumes/5cd54fb7-afc2f7da-d1a2-2c44fd82f008/',
      'provisioned': 2368357688359,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 0,
      'name': 'Nimble_VVOL3',
      'freeSpace': 0,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VVOL',
      'uncommitted': 0,
      'url': 'ds:///vmfs/volumes/vvol:0000001300004000-85a53827ddda510d/',
      'provisioned': 0,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 7696581394432,
      'name': 'Nimble_VVOL2',
      'freeSpace': 7696555180032,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VVOL',
      'uncommitted': 260064198656,
      'url': 'ds:///vmfs/volumes/vvol:0000001400004000-85a53827ddda510d/',
      'provisioned': 260090413056,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 235954765824,
      'name': 'DS-Washington-Dev3-RC3',
      'freeSpace': 110031273984,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VMFS',
      'uncommitted': 4483350994,
      'url': 'ds:///vmfs/volumes/5d1dc1d2-b5b7d440-a86c-2c44fd82f008/',
      'provisioned': 130406842834,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 3738869815050240,
      'name': 'Nimble-VVOL1',
      'freeSpace': 3738869805613056,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VVOL',
      'uncommitted': 13073285120,
      'url': 'ds:///vmfs/volumes/vvol:0000000d00004000-85a53827ddda510d/',
      'provisioned': 13082722304,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 214479929344,
      'name': 'DS-Banglore-Dev2',
      'freeSpace': 167385235456,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VMFS',
      'uncommitted': 251918164124,
      'url': 'ds:///vmfs/volumes/5d11d4f4-1e859345-2081-2c44fd82f008/',
      'provisioned': 299012858012,
      'datastore_cluster': 'N/A'
    },
    {
      'accessible': True,
      'capacity': 118916907008,
      'name': 'DS-Washington-Dev2-RC2',
      'freeSpace': 73115107328,
      'maintenanceMode': 'normal',
      'multipleHostAccess': False,
      'type': 'VMFS',
      'uncommitted': 2335867348,
      'url': 'ds:///vmfs/volumes/5cf0f6eb-65901ff8-3632-2c44fd82f008/',
      'provisioned': 48137667028,
      'datastore_cluster': 'N/A'
    }
  ],
  'invocation': {
    'module_args': {
      'hostname': '172.17.29.162',
      'username': 'administrator@vsphere.local',
      'password': 'VALUE_SPECIFIED_IN_NO_LOG_PARAMETER',
      'datacenter_name': 'Datacenter1',
      'validate_certs': False,
      'datacenter': 'Datacenter1',
      'port': 443,
      'gather_nfs_mount_info': False,
      'gather_vmfs_mount_info': False,
      'proxy_host': None,
      'proxy_port': None,
      'name': None,
      'cluster': None
    }
  },
  '_ansible_no_log': False
}

{
  'changed': False,
  'virtual_machines': [
    {
      'guest_name': 'atlas-Jun15-2024-10',
      'guest_fullname': 'CentOS 7 (64-bit)',
      'power_state': 'poweredOn',
      'ip_address': '172.17.29.168',
      'mac_address': [
        '00:50:56:9d:63:20',
        '00:50:56:9d:cf:bb',
        '00:50:56:9d:70:1a'
      ],
      'uuid': '421d7edd-b2d3-594a-f2d4-7710f1c09dfd',
      'vm_network': {
        '00:50:56:9d:63:20': {
          'ipv4': [
            '172.17.29.168'
          ],
          'ipv6': [
            
          ]
        },
        '00:50:56:9d:cf:bb': {
          'ipv4': [
            
          ],
          'ipv6': [
            
          ]
        },
        '00:50:56:9d:70:1a': {
          'ipv4': [
            
          ],
          'ipv6': [
            
          ]
        }
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'atlas-Jun8-2023-8',
      'guest_fullname': 'CentOS 7 (64-bit)',
      'power_state': 'poweredOn',
      'ip_address': '172.17.29.167',
      'mac_address': [
        '00:50:56:9d:4f:a8',
        '00:50:56:9d:14:24',
        '00:50:56:9d:ee:d5'
      ],
      'uuid': '421db583-c6ea-ddab-9357-263ab305059b',
      'vm_network': {
        '00:50:56:9d:4f:a8': {
          'ipv4': [
            '172.17.29.167'
          ],
          'ipv6': [
            
          ]
        },
        '00:50:56:9d:14:24': {
          'ipv4': [
            
          ],
          'ipv6': [
            
          ]
        },
        '00:50:56:9d:ee:d5': {
          'ipv4': [
            
          ],
          'ipv6': [
            
          ]
        }
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'atlas-Jun24-2026-5',
      'guest_fullname': 'CentOS 7 (64-bit)',
      'power_state': 'poweredOn',
      'ip_address': '172.17.29.166',
      'mac_address': [
        '00:50:56:9d:9b:57',
        '00:50:56:9d:b1:c4',
        '00:50:56:9d:95:42'
      ],
      'uuid': '421da71b-3a59-98c6-9157-2ffd3aae51e7',
      'vm_network': {
        '00:50:56:9d:9b:57': {
          'ipv4': [
            '172.17.29.166'
          ],
          'ipv6': [
            
          ]
        },
        '00:50:56:9d:b1:c4': {
          'ipv4': [
            
          ],
          'ipv6': [
            
          ]
        },
        '00:50:56:9d:95:42': {
          'ipv4': [
            
          ],
          'ipv6': [
            
          ]
        }
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'rebuild_clone_atlas_may13',
      'guest_fullname': 'CentOS 7 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:e2:1d',
        '00:50:56:9d:65:a3',
        '00:50:56:9d:cb:e6'
      ],
      'uuid': '421df8b4-0088-ab54-c474-562e395209d3',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'Windows-Server-2019',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:f1:63'
      ],
      'uuid': '421dece6-68fd-e3e6-315b-a0168f6602ea',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'atlas-May13-2020-3',
      'guest_fullname': 'CentOS 7 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:bb:1e',
        '00:50:56:9d:49:56',
        '00:50:56:9d:76:ba'
      ],
      'uuid': '421d2336-3fee-c68a-45a7-38584d5986b0',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'windows-2019',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOn',
      'ip_address': '172.17.29.163',
      'mac_address': [
        '00:50:56:9d:f5:dc'
      ],
      'uuid': '421d85f9-57f6-9082-4d01-bfbd8bb10f3b',
      'vm_network': {
        '00:50:56:9d:f5:dc': {
          'ipv4': [
            '172.17.29.163'
          ],
          'ipv6': [
            
          ]
        }
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': '3par_rcg_vm1',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:f1:bb'
      ],
      'uuid': '421dbbfc-e250-de61-9fd3-4e68135d0845',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': '3par_vvol_rc_vm1',
      'guest_fullname': None,
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:c3:a3'
      ],
      'uuid': None,
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'rcg_vm2',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:b1:ac'
      ],
      'uuid': '421d5058-27e5-2454-943d-32212518871d',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'VVOL_VM1',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:96:4b'
      ],
      'uuid': '421dabaf-370e-d240-78cd-74bbbe7a18b4',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'rmc-dev_6.3.0-1950.2',
      'guest_fullname': 'CentOS 4/5 or later (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:44:43',
        '00:50:56:9d:f2:69',
        '00:50:56:9d:b0:a9'
      ],
      'uuid': '421d3078-9cf8-89ba-ab3b-1663d1033b2d',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'VVOL_VM2',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:79:e4'
      ],
      'uuid': '421db96c-2720-85be-accc-c9dade0b48d9',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'RC_VM2',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:d6:44'
      ],
      'uuid': '421d340d-17f6-89ee-b231-8c7780deffc8',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'CBT-RMC-TEST-VM',
      'guest_fullname': 'CentOS 4/5 or later (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:f7:e1',
        '00:50:56:9d:2d:ee',
        '00:50:56:9d:68:75'
      ],
      'uuid': '421de502-99df-8aa8-f5de-e0aa14b85880',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'rmc-Nov28-2',
      'guest_fullname': 'CentOS 4/5 or later (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:1a:c2',
        '00:50:56:9d:36:37',
        '00:50:56:9d:1d:b3'
      ],
      'uuid': '421d0fd2-b236-08bf-d351-4efe1ea67da0',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'RC_VM1',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:c6:93'
      ],
      'uuid': '421d4649-e6c6-c6cb-a056-456bcf3382d4',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'vcs67',
      'guest_fullname': 'Other 3.x Linux (64-bit)',
      'power_state': 'poweredOn',
      'ip_address': '172.17.29.162',
      'mac_address': [
        '00:0c:29:40:71:de'
      ],
      'uuid': '564d991c-11e8-75a2-cfcb-2da4694071de',
      'vm_network': {
        '00:0c:29:40:71:de': {
          'ipv4': [
            '172.17.29.162'
          ],
          'ipv6': [
            
          ]
        }
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'Suse_VM',
      'guest_fullname': 'Other Linux (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:9a:91'
      ],
      'uuid': '421d23ed-f270-111b-e5d6-26aeb5f2d5d9',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'linux-tiny-vm',
      'guest_fullname': 'Other Linux (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:0c:29:0f:d2:e3'
      ],
      'uuid': '564d99e6-3fdc-709e-ca1a-80fec80fd2e3',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'ubuntu18_04',
      'guest_fullname': 'Ubuntu Linux (64-bit)',
      'power_state': 'poweredOn',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:dc:e4'
      ],
      'uuid': '421dd4e2-4f06-3165-c008-50bd6312f742',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'RC_VM3',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:11:eb'
      ],
      'uuid': '421d530f-c7b0-6515-f909-8296b7d22f22',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'Lite_OS_VM',
      'guest_fullname': 'Other Linux (32-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:a0:71'
      ],
      'uuid': '421d313a-850e-9dd2-2926-0bb82e75ff4d',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'VM2',
      'guest_fullname': 'Microsoft Windows Server 2016 (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:b0:49'
      ],
      'uuid': '421d60af-0948-defc-ad4a-187a22911299',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    },
    {
      'guest_name': 'rmc-Nov28',
      'guest_fullname': 'CentOS 4/5 or later (64-bit)',
      'power_state': 'poweredOff',
      'ip_address': '',
      'mac_address': [
        '00:50:56:9d:9e:2c',
        '00:50:56:9d:66:95',
        '00:50:56:9d:0b:c6'
      ],
      'uuid': '421d5597-c177-5e8e-fd21-e3e62d77f5ae',
      'vm_network': {
        
      },
      'esxi_hostname': '172.17.6.2',
      'cluster': None,
      'attributes': {
        
      },
      'tags': [
        
      ]
    }
  ],
  'invocation': {
    'module_args': {
      'hostname': '172.17.29.162',
      'username': 'administrator@vsphere.local',
      'password': 'VALUE_SPECIFIED_IN_NO_LOG_PARAMETER',
      'validate_certs': False,
      'port': 443,
      'vm_type': 'all',
      'show_attribute': False,
      'show_tag': False,
      'proxy_host': None,
      'proxy_port': None,
      'folder': None
    }
  },
  '_ansible_no_log': False
}
aafak@aafak-virtual-machine:~/aafak/ansible_exp$

"""
