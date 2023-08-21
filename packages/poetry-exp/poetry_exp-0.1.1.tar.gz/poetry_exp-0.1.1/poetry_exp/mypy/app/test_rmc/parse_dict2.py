import logging
LOG = logging.getLogger(__name__)
import json
from test_rmc.vm_dict_config import vm_conf_dict
def recursive_asdict(d):
    """Convert Suds object into serializable format used to convert config object."""
    out = {}
    #LOG.info('#################inside recursive_asdict d: {0}'.format(d))
    #LOG.info('#################inside recursive_asdict type(d): {0}'.format(type(d)))

    if d is None:
        return d

    #print (d)
    #print(type(d))
    #LOG.info('#################inside d.__dict__: {0}'.format(d.__dict__))
    for k, v in d.items():
        #LOG.info('#################inside recursive_asdict v: {0}'.format(v))
        if k== 'device':
            LOG.info('#################device: {0}'.format(v))
            LOG.info('#################device: {0}'.format(isinstance(v, list)))
        if k in ['dynamicType ', 'dynamicProperty ']:
            continue
        if isinstance(v, dict):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if isinstance(item, dict):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out


def recursive_asdict(d):
    """Convert dict having pyvmomi object into serializable format used to convert config object."""
    out = {}
    if d is None:
        return d

    for k, v in d.items():
        if k in ['dynamicType', 'dynamicProperty']:
            continue
        elif k == 'network':
            out[k] = {
                "_type": "Network",
                "value": v._moId
            }
        elif k == 'datastore':
            out[k] = {
                "_type": "Datastore",
                "value": v._moId
            }
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__dict__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        elif hasattr(v, '__dict__') and k != 'level' and k != 'sharedBus':
            out[k] = recursive_asdict(v)
        else:
            out[k] = v
    return out

def process_config_object(prop_dict):

    try:
        LOG.info("###############process_config_object : Enter")
        #LOG.info('################# prop_dict: {0}'.format(prop_dict))

        #conf_dict = dict(prop_dict.values()[0])
        conf_dict = prop_dict['config']
        snap_config_dict = {}
        LOG.info('################# conf_dict: {0}'.format(conf_dict))
        for ckeys in conf_dict.keys():
            if ckeys == 'alternateGuestName' or ckeys == 'annotation' or ckeys == 'changeVersion'\
                    or ckeys == 'cpuHotAddEnabled' or ckeys == 'cpuHotRemoveEnabled' or ckeys == 'guestId'\
                    or ckeys == 'vAssertsEnabled' or ckeys == 'npivTemporaryDisabled' or ckeys == 'version'\
                    or ckeys == 'guestFullName' or ckeys == 'locationId' or ckeys == 'name' or ckeys == 'npivNodeWorldWideName'\
                    or ckeys == 'npivPortWorldWideName' or ckeys == 'npivWorldWideNameType' or ckeys == 'swapPlacement'\
                    or ckeys == 'template' or ckeys == 'uuid':
                snap_config_dict[ckeys] = conf_dict[ckeys]

            elif ckeys == 'bootOptions' or ckeys == 'consolePreferences' or ckeys == 'cpuAffinity'\
                    or ckeys == 'cpuAllocation' or ckeys == 'defaultPowerOps' \
                    or ckeys == 'files' or ckeys == 'flags' or ckeys == 'memoryAffinity' \
                    or ckeys == 'memoryAllocation' or ckeys == 'tools':
                #LOG.info('#################inside boot options ckeys: {0}'.format(ckeys))
                #LOG.info('#################inside boot options conf_dict[ckeys]: {0}'.format(conf_dict[ckeys]))

                snap_config_dict[ckeys] = recursive_asdict(conf_dict[ckeys])

            elif ckeys == 'extraConfig':
                exConf_list = []
                exConf_dict = {}
                exConf_list_dict = []
                #LOG.info('#################inside extraConfig conf_dict[ckeys]: {0}'.format(conf_dict[ckeys]))

                exConf_list = conf_dict[ckeys]

                for ex in range(len(exConf_list)):
                    exConf_dict = recursive_asdict(exConf_list[ex])
                    if 'ctkEnabled' in exConf_dict:
                        LOG.info("Skipping config: "+str(exConf_dict))
                        continue
                    exConf_list_dict.append(exConf_dict)
                snap_config_dict[ckeys] = exConf_list_dict

            elif ckeys == 'hardware':
                h_dict = conf_dict[ckeys]
                for hkey in h_dict.keys():
                    if hkey == 'memoryMB' or hkey == 'numCPU' or hkey == 'numCoresPerSocket' \
                            or hkey == 'virtualICH7MPresent' or hkey == 'virtualSMCPresent':
                        snap_config_dict[hkey] = h_dict[hkey]

        if 'hardware' in conf_dict:
            #print (conf_dict['hardware'])
            hw = conf_dict['hardware'].get('device ')
            snap_config_dict['hardware'] = []
            #print(hw)
            for dev in range(len(hw)):

                device_dict = {}
                #LOG.info('#################inside hardware hw[dev]: {0}'.format(hw[dev]))
                LOG.info('#################inside hardware hw[dev].__class__.__name__: {0}'.format(hw[dev].__class__.__name__))
                device_cls_name = hw[dev].__class__.__name__  # will give the full name like vim.vm.device.VirtualIDEController
                cls_name = device_cls_name[device_cls_name.rfind('.')+1:]  # will give VirtualIDEController
                LOG.info('#################cls_name: {0}'.format(cls_name))
                if cls_name in ['VirtualDisk', 'VirtualE1000e']:
                    LOG.info('#################hw[dev]: {0}'.format(hw[dev]))
                    device_dict[cls_name] = recursive_asdict(hw[dev])
                else:
                    device_dict[cls_name] = recursive_asdict(hw[dev])
                LOG.info('#################device_dict: {0}'.format(device_dict))
                snap_config_dict['hardware'].append(device_dict)

        LOG.info('.......$$$$$$$..........snap_config_dict: {0}'.format(snap_config_dict))
        LOG.info("process_config_object : Exit")
        print(snap_config_dict)
        return snap_config_dict

    except Exception as e:
        LOG.exception("Error while processing the config object:%s", e)
        msg = "Error while processing the config object"
        raise e(msg=msg)


if __name__ =='__main__':
  d = {'config': vm_conf_dict}
  c = process_config_object(d)
  print(c)
  #s = json.dumps(c)
  #print (s)