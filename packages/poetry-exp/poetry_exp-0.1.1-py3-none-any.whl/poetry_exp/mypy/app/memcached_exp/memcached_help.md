Memcached is an in-memory key-value store for small chunks of arbitrary data
(strings, objects) from results of database calls, API calls, or page rendering.

Free & open source, high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web applications
 by alleviating database load.

Memcached is simple yet powerful. Its simple design promotes quick deployment,
ease of development, and solves many problems facing large data caches.
 Its API is available for most popular languages.


Set Proxy:

aafak@WHDCIS4TDR:~$ export http_proxy=http://web-proxy.in.hpecorp.net:8080

aafak@WHDCIS4TDR:~$ export https_proxy=http://web-proxy.in.hpecorp.net:8080

aafak@WHDCIS4TDR:~$ export HTTP_PROXY=http://web-proxy.in.hpecorp.net:8080

aafak@WHDCIS4TDR:~$ export HTTPS_PROXY=http://web-proxy.in.hpecorp.net:8080


**Install dependency from https://libevent.org/:**

aafak@WHDCIS4TDR:~/$ wget https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz
--2022-08-16 14:52:37--  https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz
Resolving web-proxy.in.hpecorp.net (web-proxy.in.hpecorp.net)... 16.242.46.30
Connecting to web-proxy.in.hpecorp.net (web-proxy.in.hpecorp.net)|16.242.46.30|:8080... connected.
Proxy request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/1856976/1524bb00-bedd-11ea-8c51-a1125df41e13?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220816%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220816T092238Z&X-Amz-Expires=300&X-Amz-Signature=74e84123a829743e2efad274b4f975bd87604aadbf9a5c94b12313f6d5f922c8&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=1856976&response-content-disposition=attachment%3B%20filename%3Dlibevent-2.1.12-stable.tar.gz&response-content-type=application%2Foctet-stream [following]
--2022-08-16 14:52:38--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/1856976/1524bb00-bedd-11ea-8c51-a1125df41e13?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220816%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220816T092238Z&X-Amz-Expires=300&X-Amz-Signature=74e84123a829743e2efad274b4f975bd87604aadbf9a5c94b12313f6d5f922c8&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=1856976&response-content-disposition=attachment%3B%20filename%3Dlibevent-2.1.12-stable.tar.gz&response-content-type=application%2Foctet-stream
Connecting to web-proxy.in.hpecorp.net (web-proxy.in.hpecorp.net)|16.242.46.30|:8080... connected.
Proxy request sent, awaiting response... 200 OK
Length: 1100847 (1.0M) [application/octet-stream]
Saving to: ‘libevent-2.1.12-stable.tar.gz’

libevent-2.1.12-stable.tar.gz              100%[========================================================================================>]   1.05M  4.75MB/s    in 0.2s

2022-08-16 14:52:39 (4.75 MB/s) - ‘libevent-2.1.12-stable.tar.gz’ saved [1100847/1100847]

aafak@WHDCIS4TDR:~/$ cd libevent-2.1.12-stable
aafak@WHDCIS4TDR:~/libevent-2.1.12-stable$ ./configure && make && sudo make install

if not works, try:
 aafak@WHDCIS4TDR:~/libevent-2.1.12-stable$ ./configure --disable-openssl
 and then
 aafak@WHDCIS4TDR:~/libevent-2.1.12-stable$ make && sudo make install
 

**Install memcahced from  https://memcached.org/:**

aafak@WHDCIS4TDR:~$ wget https://memcached.org/files/memcached-1.6.16.tar.gz
--2022-08-16 14:38:49--  https://memcached.org/files/memcached-1.6.16.tar.gz
Resolving web-proxy.in.hpecorp.net (web-proxy.in.hpecorp.net)... 16.242.46.30
Connecting to web-proxy.in.hpecorp.net (web-proxy.in.hpecorp.net)|16.242.46.30|:8080... connected.
Proxy request sent, awaiting response... 200 OK
Length: 1054877 (1.0M) [application/octet-stream]
Saving to: ‘memcached-1.6.16.tar.gz’

memcached-1.6.16.tar.gz                    100%[========================================================================================>]   1.01M   845KB/s    in 1.2s

2022-08-16 14:38:52 (845 KB/s) - ‘memcached-1.6.16.tar.gz’ saved [1054877/1054877]

aafak@WHDCIS4TDR:~$ ls
memcached-1.6.16.tar.gz  test.py
aafak@WHDCIS4TDR:~$ tar -xvzf memcached-1.6.16.tar.gz
aafak@WHDCIS4TDR:~$ cd memcached-1.6.16/
aafak@WHDCIS4TDR:~/memcached-1.6.16$ 
aafak@WHDCIS4TDR:~/memcached-1.6.16$ ./configure && make && make test && sudo make install


aafak@WHDCIS4TDR:~/memcached-1.6.16$ memcached -d -m 1024 -u root -l 127.0.0.1 -p 11211