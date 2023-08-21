Alembic provides for the creation, management, and invocation of change management scripts
for a relational database, using SQLAlchemy as the underlying engine

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic init alembic
Creating directory C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic ...  done
Creating directory C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic\versions ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic.ini ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic\env.py ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic\README ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic\script.py.mako ...  done
Please edit configuration/connection/logging settings in 'C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\sqlalchemey_exp\\alembic_db_migration_exp2\\alembic.ini' before proceeding.

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2


Add following code in env.py:
###########Start Added by me###
db_config = {
    'drivername': 'postgresql',
    'host': '172.17.81.12',
    'username': 'postgres',
    'password': 'test',
    'database': 'mycloud',
    'port': 5432
}
db_connection_url = f"{db_config['drivername']}://{db_config['username']}:" \
    f"{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

config.set_main_option("sqlalchemy.url", db_connection_url)



aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic revision -m "Create_mycloud_tables"
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic\versions\b845c9f7e714_create_mycloud_tables.py ...  done

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2

Rename file with 0001 and update the version 0001 and update the downgrade and upgrade method


First create database mycloud2:
aafak@aafak-rnd-vm:~$ psql -h localhost -U postgres
Password for user postgres:
psql (12.12 (Ubuntu 12.12-0ubuntu0.20.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=# create database mycloud2;
CREATE DATABASE

Now run first migration:

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0001, Create_mycloud_tables

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2


Now verify the database:
postgres=# \c mycloud2;
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
You are now connected to database "mycloud2" as user "postgres".
mycloud2=# \d
                List of relations
 Schema |       Name        |   Type   |  Owner
--------+-------------------+----------+----------
 public | alembic_version   | table    | postgres
 public | datastores        | table    | postgres
(3 rows)

mycloud2=# select * from alembic_version;
 version_num
-------------
 0001
(1 row)

mycloud2=#


Now add new column:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic revision -m "Add created_at column"
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp2\alembic\versions\14e32a17a88a_add_created_at_column.py ...  done

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$

Now rename the file 14e32a17a88a_add_created_at_column.py to 0002_add_created_at_column.py and update it

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('datastores', sa.Column('created_at', sa.DateTime))


def downgrade():
    op.drop_column('datastores', 'created_at')
    

Now run migration:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 0001 -> 0002, Add created_at column

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2

Now verify the database:
mycloud2=# select * from alembic_version;
 version_num
-------------
 0002
(1 row)

mycloud2=# \d datastores
                                         Table "public.datastores"
   Column    |            Type             | Collation | Nullable |                Default
-------------+-----------------------------+-----------+----------+----------------------------------------
 id          | integer                     |           | not null | 
 name        | character varying(50)       |           | not null |
 description | character varying(200)      |           |          |
 created_at  | timestamp without time zone |           |          |
Indexes:
    "datastores_pkey" PRIMARY KEY, btree (id)

mycloud2=#


Now downgrade:

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic downgrade base
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 0002 -> 0001, Add created_at column
INFO  [alembic.runtime.migration] Running downgrade 0001 -> , Create_mycloud_tables

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2


mycloud2=# \d
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
(1 row)

mycloud2=#
mycloud2=# select * from alembic_version;
 version_num
-------------
(0 rows)

mycloud2=#


aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0001, Create_mycloud_tables
INFO  [alembic.runtime.migration] Running upgrade 0001 -> 0002, Add created_at column

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2
$ alembic downgrade -1
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 0002 -> 0001, Add created_at column

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp2

mycloud2=# select * from alembic_version;
 version_num
-------------
 0001
(1 row)

mycloud2=# \d datastores;
                                      Table "public.datastores"
   Column    |          Type          | Collation | Nullable |                Default
-------------+------------------------+-----------+----------+----------------------------------------
 id          | integer                |           | not null | 
 
 name        | character varying(50)  |           | not null |
 description | character varying(200) |           |          |
Indexes:
    "datastores_pkey" PRIMARY KEY, btree (id)

mycloud2=#


mycloud2=# \d
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | datastores      | table | postgres
(2 rows)

mycloud2=#

