Install postgres:
https://adamtheautomator.com/install-postgresql-on-a-ubuntu/

`sudo apt install -y postgresql postgresql-contrib postgresql-client
`

aafak@aafak-rnd-vm:~$ sudo systemctl status postgresql.service
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (exited) since Tue 2022-08-23 10:52:03 IST; 1min 10s ago
   Main PID: 3001734 (code=exited, status=0/SUCCESS)
      Tasks: 0 (limit: 11866)
     Memory: 0B
     CGroup: /system.slice/postgresql.service

Aug 23 10:52:03 aafak-rnd-vm systemd[1]: Starting PostgreSQL RDBMS...

Change the password:

postgres=#
afak@aafak-rnd-vm:~$ sudo -u postgres psql
psql (12.12 (Ubuntu 12.12-0ubuntu0.20.04.1))
Type "help" for help.

postgres=# \password postgres
Enter new password for user "postgres":test
Enter it again:test
postgres=#


postgres=# create database mycloud;
CREATE DATABASE
postgres=# \c mycloud;
You are now connected to database "mycloud" as user "postgres".
mycloud=#


mycloud=# create table test(id int, name varchar);
CREATE TABLE
mycloud=#

mycloud=# insert into test values(1, 'A');
INSERT 0 1
mycloud=# select * from test;
 id | name
----+------
  1 | A
(1 row)


aafak@aafak-rnd-vm:~$ sudo vim /etc/postgresql/12/main/postgresql.conf

listen_addresses = '*'

save the file

aafak@aafak-rnd-vm:~$ sudo vim /etc/postgresql/12/main/pg_hba.conf
Change followingtwo line: by

host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5

with:
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5


sudo service postgresql restart


