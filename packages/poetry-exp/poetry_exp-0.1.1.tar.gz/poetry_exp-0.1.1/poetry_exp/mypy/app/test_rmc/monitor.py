import time
import string
import sys
import commands

def get_cpumem(pid):
    d = [i for i in commands.getoutput("ps aux").split("\n")
        if i.split()[1] == str(pid)]
    return (float(d[0].split()[2]), float(d[0].split()[3])) if d else None


if __name__ == '__main__':
    if not len(sys.argv) == 2 or not all(i in string.digits for i in sys.argv[1]):
        print("usage: %s PID" % sys.argv[0])
        exit(2)
    print("%CPU\t%MEM")
    try:
        while True:
            x,y = get_cpumem(sys.argv[1])
            if not x:
                print("no such process")
                exit(1)
            print("%.2f\t%.2f" % (x,y))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print
        exit(0)


"""
[root@rmc-jul3 ~]# ps -aux | grep test.p
root     27640  0.7 18.4 3087988 2966920 pts/1 T    09:05   0:02 python test.py
root     28742  1.2  0.5 210708 89848 pts/4    S+   09:11   0:00 python test.py
root     28754  0.0  0.0 112712   984 pts/1    S+   09:11   0:00 grep --color=auto test.p
[root@rmc-jul3 ~]# python monitor.py 27640
%CPU    %MEM
0.70    18.40
0.70    18.40
0.70    18.40
0.70    18.40
0.70    18.40
0.70    18.40
0.70    18.40

"""
