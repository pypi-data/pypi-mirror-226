"""
[root@rmc-jul3 ~]# cat monitor.sh
while sleep 1; do  ps -p $1 -o pcpu= -o pmem= ; done;

[root@rmc-jul3 ~]# ps -aux | grep test.py
root     22411  0.5  5.1 946688 825620 pts/1   S+   08:35   0:00 python test.py
root     23243  0.0  0.0 112708   984 pts/3    S+   08:38   0:00 grep --color=auto test.py
[root@rmc-jul3 ~]#
[root@rmc-jul3 ~]# ./monitor.sh 22411
 0.5  5.9
 0.5  5.9
 0.5  6.0
 0.5  6.0
 0.5  6.0
^C[root@rmc-jul3 ~]#

"""


import time
a = []
while True:
    print len(a)
    a.append(' ' * 10**6)
    time.sleep(0.2)
