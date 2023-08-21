import os
from subprocess import Popen, PIPE
import yaml

FS_CROWLER_CONFIG_BASE_DIR = "/tmp/fscrawler"

DEFAULT_SETTINGS_DIR = "/root/.fscrawler/"
DEFAULT_SETTINGS_PATH = DEFAULT_SETTINGS_DIR + "{0}/_settings.yaml"
FS_CROWLER_PATH = "/usr/aafak/fscrawler-es7-2.7-SNAPSHOT/bin/fscrawler "

FS_CROWLER_CMD = FS_CROWLER_PATH + "{0} --loop 1"
ES_URL = "http://172.17.29.167:9200"

MOUNT_DIR = "/tmp/fs_indices/{0}/{1}/dev{2}"


def start_fs_crowler(index_name, dir_path):
    print('Creating file system crowler job...')
    cmd = "printf 'y\ny\ny\n' | " + FS_CROWLER_PATH + index_name
    #cmd = "printf 'y\ny\ny\n' | " + FS_CROWLER_PATH + snap_id
    os.system(cmd)

    edit_config_file(DEFAULT_SETTINGS_PATH.format(index_name), dir_path, ES_URL)
    #edit_config_file(DEFAULT_SETTINGS_PATH.format(snap_id), snap_id, dir_path, ES_URL)

    print('Starting file system crowler job: {0} ...'.format(index_name))
    os.system(FS_CROWLER_CMD.format(index_name))
    #os.system(FS_CROWLER_CMD.format(snap_id))


def edit_config_file(file_path, dir_path, es_url):
    print("Updating the crowler job config: {0}...".format(file_path))

    with open(file_path) as f:
        doc = yaml.load(f)

    print(doc)
    #doc['name'] = index_name
    fs = doc['fs']
    fs['url'] = dir_path
    fs['index_content'] = False
    fs['external'] = {
        "snapId": "sanp1"
    }

    elasticsearch = doc['elasticsearch']
    elasticsearch['nodes'][0]['url'] = es_url

    with open(file_path, "w") as f:
        yaml.dump(doc, f)

    print('Successfully updated the file system crowler job config file')


def exe_cmd2(cmd):
    print('Excecuting cmd: {0}...'.format(cmd))
    output = os.popen(cmd).read()
    return output


def get_device_list():
    cmd = "blkid | awk '{print $1}' | sed 's/.$//'"
    output = exe_cmd2(cmd)
    devices = output.split('\n')
    return devices


def get_device_serial_num(device_list):
    result = dict()
    for device in device_list:
        if len(device) >1:
            cmd = "sg_inq " + device + " | grep 'Unit serial number:' | awk '{print $4}'"
            print(cmd)
            output = exe_cmd2(cmd)
            result[device] = output[0:-1]
    return result


def get_device_paths(disk_ids):
    dev_paths = []
    device_list = get_device_list()
    print("Device list: {0}".format(device_list))
    device_serial_nums = get_device_serial_num(device_list)
    print("Device serial numbers: {0}".format(device_serial_nums))
    for dev_path, device_serial_num in device_serial_nums.items():
        print("Device: {0}, Sr #{1} in disk ids: {2}, matched: {3}".format(
            dev_path, device_serial_num, disk_ids, (device_serial_num in disk_ids)))
        if device_serial_num in disk_ids:
            dev_paths.append(dev_path)
    print("Device paths to mount: {0}".format(dev_paths))
    return dev_paths


def mount_disks(disk_ids, snapshot_info):
    dev_paths = get_device_paths(disk_ids)
    mount_paths = []
    try:
        for i in range(1, len(dev_paths)):
            snap_id = snapshot_info['id']
            snap_name = snapshot_info['name']
            mount_path = MOUNT_DIR.format(snap_id, snap_name, i)
            print('Creating mount dir: {0}...'.format(mount_path))
            os.makedirs(mount_path, exist_ok=True)
            print('Mounting device: {0} with dir: {1}...'.format(dev_paths[i], mount_path))
            mount_cmd = 'mount {0} {1}'.format(dev_paths[i], mount_path)
            exe_cmd2(mount_cmd)
            mount_paths.append(mount_path)
    except Exception as e:
        delete_mount_points(mount_paths)
        raise Exception('Failed to mount disks: {0}'.format(disk_ids))

    return mount_paths


def delete_mount_points(mount_paths):
    if mount_paths:
        for mount_path in mount_paths:
            if os.path.exists(mount_path):
                print('Un mounting path : {0}'.format(mount_path))
                try:
                    exe_cmd2('umount ' + mount_path)
                except Exception as e:
                    print("ERROR: Failed to un mount,"
                          " error: {0}".format(str(e)))
                print('Deleting mount path : {0}'.format(mount_path))
                try:
                    exe_cmd2('rm -rf ' + mount_path)
                except Exception as e:
                    print("ERROR: Failed to delete mount path,"
                          " error: {0}".format(str(e)))


def delete_fs_crowl_job(vm_id):
    job_config_dir = DEFAULT_SETTINGS_DIR + vm_id
    if os.path.exists(job_config_dir):
        print('Deleting file system crowler job config... : {0}'.format(job_config_dir))
        exe_cmd2('rm -rf ' + DEFAULT_SETTINGS_DIR + vm_id)
    else:
        print('No file system crowler job found for path : {0}'.format(job_config_dir))


def mount_and_crowl(vm_id, disk_ids, snapshot_info):
    vm_id = vm_id.lower()
    disk_ids = [(id.replace("-", "")).lower() for id in disk_ids]
    print('Virtual machine disk ids: {0}'.format(disk_ids))

    snap_id = snapshot_info['id']
    delete_fs_crowl_job(vm_id)
    #delete_fs_crowl_job(snap_id)
    mount_paths = []
    try:
        mount_paths = mount_disks(disk_ids, snapshot_info)
        for mount_path in mount_paths:
            start_fs_crowler(vm_id, mount_path)
    except Exception as e:
        raise Exception('Failed to start file system crowler,'
                        ' error: {0}'.format(str(e)))
    finally:
        delete_mount_points(mount_paths)
        delete_fs_crowl_job(vm_id)
        #delete_fs_crowl_job(snap_id)

if __name__ == '__main__':
   # edit_config_file('settings.yml', '/mnt/aafak1', "http://172.17.29.167:9300")
   #start_fs_crowler('vm2', '/mnt/Users')
   #device_list = get_device_list()
   #get_device_serial_num(device_list)
   #mount_disks(['6000c295791b213568243083ddb5ad5c'])
   snap_info = {
       'id': 'fd4d12f4-b31c-4263-ae50-5246f46c19a1',
       'name': '26-Aug-20T15:09'
   }
   #mount_and_crowl('6000C295-791b-2135-6824-3083ddb5ad6c', ["6000C295-791b-2135-6824-3083ddb5ad5c"], snap_info)

   mount_and_crowl('vm1', ["6000C295-791b-2135-6824-3083ddb5ad5c"], snap_info)