import psutil
import time
import sys
from datetime import datetime


def monitor_process(pid):
    p = psutil.Process(pid)
    while True:
        print  datetime.now(), ' Mem %: ', p.get_memory_percent(), 'cpu %: ', p.get_cpu_percent(), ' threads# ', p.num_threads()
        time.sleep(60*30)


if __name__ == '__main__':
    args = sys.argv
    pid = args[1]
    monitor_process(int(pid))


"""
[root@rmc-jul3 ~]# ps -aux | grep python3
root      2143  0.0  0.1 228356 20920 ?        Ss   09:49   0:00 /usr/bin/python3 /usr/local/bin/gunicorn --workers=1 --threads=5 --ssl-version=5 -c /etc/rmv/rmcv_app_v2_gunicorn.conf rmcv_app_v2.wsgi:application
root      2155  0.1  0.3 762704 61444 ?        Sl   09:49   0:01 /usr/bin/python3 /usr/local/bin/gunicorn --workers=1 --threads=5 --ssl-version=5 -c /etc/rmv/rmcv_app_v2_gunicorn.conf rmcv_app_v2.wsgi:application


[root@rmc-jul3 ~]# stdbuf -oL python monitor_process.py 2155 >  memory_usage.log &
[root@rmc-jul3 ~]# tail -f memory_usage.log
2019-07-05 14:48:46.286553  Mem %:  0.482178667472 cpu %:  1.0  threads#  7
2019-07-05 14:48:47.288625  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:48.290270  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:49.293195  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:50.295089  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:51.296122  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:52.297996  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:53.299152  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:54.301214  Mem %:  0.482178667472 cpu %:  0.0  threads#  7
2019-07-05 14:48:55.302736  Mem %:  0.482178667472 cpu %:  0.0  threads#  7


>>> p = psutil.Process(32490)
>>> dir(p)
['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_create_time', '_exe', '_gone', '_hash', '_ident', '_init', '_last_proc_cpu_times', '_last_sys_cpu_times', '_name', '_pid', '_ppid', '_proc', '_send_signal', 'as_dict', 'children', 'cmdline', 'connections', 'cpu_affinity', 'cpu_percent', 'cpu_times', 'create_time', 'cwd', 'exe', 'get_children', 'get_connections', 'get_cpu_affinity', 'get_cpu_percent', 'get_cpu_times', 'get_ext_memory_info', 'get_io_counters', 'get_ionice', 'get_memory_info', 'get_memory_maps', 'get_memory_percent', 'get_nice', 'get_num_ctx_switches', 'get_num_fds', 'get_num_threads', 'get_open_files', 'get_rlimit', 'get_threads', 'getcwd', 'gids', 'io_counters', 'ionice', 'is_running', 'kill', 'memory_info', 'memory_info_ex', 'memory_maps', 'memory_percent', 'name', 'nice', 'num_ctx_switches', 'num_fds', 'num_threads', 'open_files', 'parent', 'pid', 'ppid', 'resume', 'rlimit', 'send_signal', 'set_cpu_affinity', 'set_ionice', 'set_nice', 'set_rlimit', 'status', 'suspend', 'terminal', 'terminate', 'threads', 'uids', 'username', 'wait']
        # CPU % is not accurate here, Memory telling correct
        # Following script can be used for CPY
        # cat monitor.sh
        # while sleep 1; do  ps -p $1 -o pcpu= -o pmem=; done;
"""