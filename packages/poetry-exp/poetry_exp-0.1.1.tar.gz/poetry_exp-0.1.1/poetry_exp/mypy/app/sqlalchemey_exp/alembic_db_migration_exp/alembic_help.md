https://alembic.sqlalchemy.org/en/latest/tutorial.html

First Install alembeic:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp$
$ pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 alembic
Requirement already satisfied: alembic in c:\python3\lib\site-packages (1.3.2)
Requirement already satisfied: SQLAlchemy>=1.1.0 in c:\python3\lib\site-packages (from alembic) (1.3.12)
Requirement already satisfied: Mako in c:\python3\lib\site-packages (from alembic) (1.1.0)
Requirement already satisfied: python-editor>=0.3 in c:\python3\lib\site-packages (from alembic) (1.0.4)
Requirement already satisfied: python-dateutil in c:\python3\lib\site-packages (from alembic) (2.8.0)
Requirement already satisfied: MarkupSafe>=0.9.2 in c:\python3\lib\site-packages (from Mako->alembic) (1.1.1)
Requirement already satisfied: six>=1.5 in c:\python3\lib\site-packages (from python-dateutil->alembic) (1.12.0)


generate a migrations directory called alembic:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp
$ alembic init alembic
Creating directory C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic ...  done
Creating directory C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic\versions ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic.ini ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic\env.py ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic\README ...  done
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic\script.py.mako ...  done
Please edit configuration/connection/logging settings in 'C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\sqlalchemey_exp\\alembic_db_migration_exp\\alembic.ini' before proceeding.

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp


Edit env.py:
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



Create first migration:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp
$ alembic revision -m "create account table"
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic\versions\cf6f24cd8d39_create_account_table.py ...  done

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp


Now provide the implentation fro upgrade and downgrade method:
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('account')
    

Now run first migration:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> cf6f24cd8d39, create account table

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp

Now verify the database:
aafak@aafak-rnd-vm:~$ psql -h localhost -U postgres
Password for user postgres:
psql (12.12 (Ubuntu 12.12-0ubuntu0.20.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=# \c mycloud;
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
You are now connected to database "mycloud" as user "postgres".
mycloud=# \d
               List of relations
 Schema |      Name       |   Type   |  Owner
--------+-----------------+----------+----------
 public | account         | table    | postgres
 public | account_id_seq  | sequence | postgres
 public | alembic_version | table    | postgres
 public | backups         | table    | postgres
 public | backups_id_seq  | sequence | postgres
 public | test            | table    | postgres
(6 rows)

mycloud=# \d account;
                                      Table "public.account"
   Column    |          Type          | Collation | Nullable |               Default
-------------+------------------------+-----------+----------+-------------------------------------
 id          | integer                |           | not null | nextval('account_id_seq'::regclass)
 name        | character varying(50)  |           | not null |
 description | character varying(200) |           |          |
Indexes:
    "account_pkey" PRIMARY KEY, btree (id)

mycloud=#

mycloud=# select * from alembic_version;
 version_num
--------------
 cf6f24cd8d39
(1 row)

mycloud=#


Running second migration:
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp
$ alembic revision -m "Add a column"
Generating C:\Users\aafakmoh\OneDrive - Hewlett Packard Enterprise\mypy\app\sqlalchemey_exp\alembic_db_migration_exp\alembic\versions\b593c38e9e00_add_a_column.py ...  done

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp

Now provide the implementaion for the b593c38e9e00_add_a_column.py 

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
    

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade cf6f24cd8d39 -> b593c38e9e00, Add a column

aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/sqlalchemey_exp/alembic_db_migration_exp
Now verify the database:

mycloud=# \d account;
                                              Table "public.account"
        Column         |            Type             | Collation | Nullable |               Default
-----------------------+-----------------------------+-----------+----------+-------------------------------------
 id                    | integer                     |           | not null | nextval('account_id_seq'::regclass)
 name                  | character varying(50)       |           | not null |
 description           | character varying(200)      |           |          |
 last_transaction_date | timestamp without time zone |           |          |
Indexes:
    "account_pkey" PRIMARY KEY, btree (id)

mycloud=#
