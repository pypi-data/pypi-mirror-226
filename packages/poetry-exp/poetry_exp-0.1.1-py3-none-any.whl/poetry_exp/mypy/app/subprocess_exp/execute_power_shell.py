from subprocess import Popen, PIPE


def execute_cmd(cmd, timeout=10):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    rc = p.wait() # will wait for the process to finish and return the exit code
    print rc
    if rc == 0:
        for line in p.stdout:
            print line
    else:
        for line in p.stderr:
            print line


if __name__ == '__main__':
    #execute_cmd('powershell ls')
    execute_cmd('powershell .\powershell_script.ps1')


"""
C:\Python27\python.exe C:/Users/mohama30/Documents/EMC/repository/personal/cb-python/cb-python/python-demo/python-program/subprocess/program/execute_power_shell.py
0




    Directory: C:\Users\mohama30\Documents\EMC\repository\personal\cb-python\cb-python\python-demo\python-program\subpr

    ocess\program





Mode                LastWriteTime         Length Name                                                                  

----                -------------         ------ ----                                                                  

-a----        7/25/2018  10:20 AM           3605 execute_cmd.py                                                        

-a----        8/15/2018  10:23 PM            500 execute_power_shell.py                                                

-a----        2/24/2016  10:34 AM             95 myshellscript.sh                                                      

-a----        8/15/2018  10:21 PM              2 powershell_script.ps1                                                 

-a----        7/25/2018   9:54 AM             95 python_script.py                                                      






Process finished with exit code 0


"""