from sqlalchemy import create_engine, select, insert, delete, update, func, text, and_
from sqlalchemy.engine.url import URL
from sqlalchemy import MetaData
from app.sqlalchemey_exp.db_crud.models import Base
import uuid

# DB_CONFIG = {
#     'driver': 'postgresql',
#     'host': '127.0.0.1',
#     'username': 'datum',
#     'password': 'hpinvent',
#     'database': 'datum',
#     'port': 5432
#
# }

DB_CONFIG = {
    'drivername': 'postgresql',
    'host': '172.17.81.12',
    'username': 'postgres',
    'password': 'test',
    'database': 'mycloud',
    'port': 5432
}

engine = create_engine(URL(**DB_CONFIG), pool_size=20, max_overflow=0)
#engine = create_engine(URL(**DB_CONFIG), pool_size=20, max_overflow=0, timeout=0)

#engine = create_engine(URL(**DB_CONFIG))
#Base.metadata.create_all(bind=engine)

meta = MetaData()
meta.reflect(bind=engine)

tables = meta.tables


def get_records(table):
    table_obj = tables[table]
    sel_query = select([table_obj])
    with engine.connect() as conn:
        result = conn.execute(sel_query)
        result_dict = [dict(_row) for _row in result]
        print(result_dict)
        return result_dict


def get_records_group_by_columns(table, columns=[]):
    table_obj = tables[table]
    group_by_cols = [text(col) for col in columns]
    select_cols = []
    select_cols.extend(group_by_cols)
    select_cols.append(func.count(table_obj.c.id))
    sel_query = select(select_cols).group_by(*group_by_cols)
    with engine.connect() as conn:
        result = conn.execute(sel_query)
        results = list(result)
        print(results)
        return results


def get_record(table, record_id):
    table_obj = tables[table]
    sel_query = select([table_obj]).where(table_obj.c.id == record_id)
    with engine.connect() as conn:
        result = conn.execute(sel_query)
        result_dict = [dict(_row) for _row in result]
        print(result_dict)
        return result_dict


def insert_record(table, values):
    table_obj = tables[table]
    ins_query = insert(table_obj)
    with engine.connect() as conn:
        conn.execute(ins_query, values)


def delete_record(table, record_id):
    table_obj = tables[table]
    del_query = delete(table_obj).where(table_obj.c.id==record_id)
    with engine.connect() as conn:
        conn.execute(del_query)


def update_record(table, record_id, values):
    table_obj = tables[table]
    update_query = update(table_obj).where(table_obj.c.id == record_id).values(values)
    with engine.connect() as conn:
        conn.execute(update_query, values)

def update_record_with_where_clouse(table, record_id, values):
    table_obj = tables[table]
    where_clause = list()
    where_clause.append(table_obj.c.id.__eq__(record_id))
    where_clause.append(table_obj.c.backup_type.__eq__('Snapshot'))
    update_query = (
        update(table_obj).where(and_(*where_clause)).values(values)
    )
    print(f'update query: {update_query}')
    with engine.connect() as conn:
        update_result = conn.execute(update_query)
        print(f'update_result: {update_result}')
        print(f'rowcount: {update_result.rowcount}')  # will be 1 if updated else 0
        print(f'process_rows: {update_result.process_rows}')  # will be again an object
        print(f'returns_rows: {update_result.returns_rows}')  # returns False in both case

"""

update query: UPDATE backups SET name=:name WHERE backups.id = :id_1 AND backups.backup_type = :backup_type_1
update_result: <sqlalchemy.engine.result.ResultProxy object at 0x040F6F30>
rowcount: 1
process_rows: <bound method ResultProxy.process_rows of <sqlalchemy.engine.result.ResultProxy object at 0x040F6F30>>
returns_rows: False
[{'id': 29, 'name': 'Bkp222_update5555', 'backup_type': 'Snapshot'}]
print(f'update_result: {dir(update_result)}')

update_result: ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
 '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
  '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
  '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
   '__subclasshook__', '__weakref__', '_autoclose_connection', '_cursor_description', 
   '_echo', '_fetchall_impl', '_fetchmany_impl', '_fetchone_impl', '_getter', '_has_key',
    '_init_metadata', '_metadata', '_non_result', '_process_row', '_saved_cursor', 
    '_soft_close', '_soft_closed', 'close', 'closed', 'connection', 'context',
     'cursor', 'dialect', 'fetchall', 'fetchmany', 'fetchone', 'first', 'inserted_primary_key',
      'is_insert', 'keys', 'last_inserted_params', 'last_updated_params', 
      'lastrow_has_defaults', 'lastrowid', 'next', 'out_parameters', 'postfetch_cols', 
      'prefetch_cols', 'process_rows', 'returned_defaults', 'returns_rows', 'rowcount',
       'scalar', 'supports_sane_multi_rowcount', 'supports_sane_rowcount']

"""

if __name__ == '__main__':
    table_name = 'backups'
    # insert_record(table_name, {"name": "Bkp1", "backup_type": "Snapshot"})
    # insert_record(table_name, {"name": "Bkp2", "backup_type": "Snapshot"})
    # insert_record(table_name, {"name": "Bkp3", "backup_type": "Snapshot"})
    # insert_record(table_name, {"name": "Bkp4", "backup_type": "LocalBackup"})
    # insert_record(table_name, {"name": "Bkp5", "backup_type": "LocalBackup"})
    # insert_record(table_name, {"name": "Bkp6", "backup_type": "LocalBackup"})
    # insert_record(table_name, {"name": "Bkp7", "backup_type": "LocalBackup"})
    # insert_record(table_name, {"name": "Bkp8", "backup_type": "CloudBackup"})
    # insert_record(table_name, {"name": "Bkp9", "backup_type": "CloudBackup"})
    #
    #get_records(table_name)
    # get_record(table_name, 2)
    #update_record(table_name, 29, {"name": "Bkp222"})
    update_record_with_where_clouse(table_name, 29, {"name": "Bkp222_update5555"})
    get_record(table_name, 29)
    # get_records_group_by_columns(table_name, ['backup_type'])  # [('CloudBackup', 2), ('Snapshot', 3), ('LocalBackup', 4)]
    # # delete_record(table_name, 1)
    # get_records(table_name)   # [{'id': 2, 'name': 'Bkp2'}]



"""
aafak@aafak-rnd-vm:~$ sudo -i -u postgres
[sudo] password for aafak:
postgres@aafak-rnd-vm:~$ psql
psql (12.14 (Ubuntu 12.14-0ubuntu0.20.04.1))
Type "help" for help.
postgres=# \l
                             List of databases
   Name    |  Owner   | Encoding | Collate | Ctype |   Access privileges
-----------+----------+----------+---------+-------+-----------------------
 mycloud   | postgres | UTF8     | en_IN   | en_IN |
 postgres  | postgres | UTF8     | en_IN   | en_IN |
 template0 | postgres | UTF8     | en_IN   | en_IN | =c/postgres          +
           |          |          |         |       | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_IN   | en_IN | =c/postgres          +
           |          |          |         |       | postgres=CTc/postgres
(4 rows)

postgres=# \c mycloud
You are now connected to database "mycloud" as user "postgres".
mycloud=# select * from backups;
 id |  name  | backup_type
----+--------+-------------
 30 | Bkp2   | Snapshot
 31 | Bkp3   | Snapshot
 32 | Bkp4   | LocalBackup
 33 | Bkp5   | LocalBackup


"""