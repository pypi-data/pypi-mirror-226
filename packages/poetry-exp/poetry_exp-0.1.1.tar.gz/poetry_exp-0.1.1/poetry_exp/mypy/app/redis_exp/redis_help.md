https://developer.redis.com/develop/python/
https://realpython.com/python-redis/

Redis is an open source, in-memory, key-value data store most commonly used as a primary database,
cache, message broker, and queue. Unlike relational databases, Redis database delivers sub-millisecond
response times, enabling fast and powerful real-time applications in industries such as gaming,
fintech, ad-tech, social media, healthcare, and IoT.

Redis (also called remote dictionary server) is a multi-model database,
and provides several built-in data structures/data type such as Lists, Hashes,
Geospatial indexes, Strings, Sets etc. You can either run Redis server in a Docker
container or directly on your machine


Install on windows:
https://developer.redis.com/create/windows/

**Step 1: Turn on Windows Subsystem for Linux:**
Open PowerShell as Administrator and run this command to enable Windows Subsystem for Linux (WSL):

`Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
`

PS C:\windows\system32>  Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Do you want to restart the computer to complete this operation now?
[Y] Yes  [N] No  [?] Help (default is "Y"):

Reboot Windows after making the change — note that you only need to do this once.

**Step 2: Launch Microsoft Windows Store**

` start ms-windows-store:
`
After reboot, start powersehell:
PS C:\windows\system32>  start ms-windows-store:
PS C:\windows\system32> it will start one UI, you can search for ubuntu and install it
 
on launch: set the password
Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username: aafak
New password:
Retype new password:
passwd: password updated successfully
Installation successful! 

Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 4.4.0-43-Microsoft x86_64)

  System load:    0.52      Users logged in:        0
  Usage of /home: unknown   IPv4 address for eth3:  192.168.56.1
  Memory usage:   55%       IPv4 address for eth4:  192.168.190.1
  Swap usage:     0%        IPv4 address for eth5:  192.168.232.1
  Processes:      6         IPv4 address for wifi0: 10.76.80.7

To check for new updates run: sudo apt update

aafak@WHDCIS4TDR:~$

set proxy:
aafak@WHDCIS4TDR:~$ sudo vim /etc/apt/apt.conf.d/proxy.conf
Acquire {
    HTTP::proxy "http://web-proxy.sdc.hpecorp.net:8080";
    HTTPS::proxy "http://web-proxy.sdc.hpecorp.net:8080";
}

aafak@WHDCIS4TDR:~$sudo apt update
aafak@WHDCIS4TDR:~$sudo apt install redis-server
aafak@WHDCIS4TDR:~$  sudo service redis-server restart
Stopping redis-server: redis-server.
Starting redis-server: redis-server.
aafak@WHDCIS4TDR:~$
aafak@WHDCIS4TDR:~$ sudo service redis-server status
 * redis-server is running
aafak@WHDCIS4TDR:~$

aafak@WHDCIS4TDR:~$ redis-cli
127.0.0.1:6379>

aafak@WHDCIS4TDR:~$ redis-cli
127.0.0.1:6379> set user aafak
OK
127.0.0.1:6379> get user
"aafak"
127.0.0.1:6379>

Please note: By default, Redis has 0-15 indexes for
databases, you can change that number databases NUMBER in redis.conf.


$ pip3 install redis --proxy=http://web-proxy.in.hpecorp.net:8080

127.0.0.1:6379> set user aafak2 NX     (set only if not exist)
(nil)
127.0.0.1:6379> set user aafak2 XX
OK
127.0.0.1:6379> set user aafak2 NX
(nil)
127.0.0.1:6379>

127.0.0.1:6379> get user2
(nil)
127.0.0.1:6379>