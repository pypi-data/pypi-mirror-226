from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import func, select
import json

from sqlalchemy.orm import (
    sessionmaker,
    scoped_session)

# https://riptutorial.com/postgresql/example/5195/using-jsonb-operators
DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'

engine = create_engine(DB_CONN_URL)
print(engine)

Base = declarative_base()


class ProtectionGroups(Base):
    __tablename__ = 'test_pg'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String)
    details = Column(JSON)
    deleted = Column(Boolean)

    def __init__(self, customer_id, details, deleted):
        self.customer_id = customer_id
        self.details = details
        self.deleted = deleted

    def __str__(self):
        return 'User: id:{0}, customer_id:{1}, details: {2}'.format(self.id, self.customer_id, self.details)



"""Uncomment following to create the table"""
# Base.metadata.create_all(bind=engine)
# print(f'Created the table')

session = scoped_session(sessionmaker(bind=engine))


protection_groups = [
    ({"customerId": "cust1", "name": "pg1", "appType": "VMware", "vmProtectionGroupType": "Custom",
      "assetsCategory": "VvolVms"},),
    ({"customerId": "cust1", "name": "pg2", "appType": "VMware", "vmProtectionGroupType": "Custom",
      "assetsCategory": "VmfsVms"},),

    ({"customerId": "cust2", "name": "pg3", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}},),

    ({"customerId": "cust2", "name": "pg4", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms",
                        "type": "VMwareVvolContainer"}},),

    ({"customerId": "cust2", "name": "pg5", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms",
                        "type": "VMwareVvolContainer"}},)
]


# for pg in protection_groups:
#     print(f"@@@@@@@@@@@@@pg: {pg}")
#
#     print(f"@@@@@@@@@@@@@custid: {pg[0]['customerId']}")
#     pg_obj = ProtectionGroups(pg[0]['customerId'], pg[0],  False)
#     session.add(pg_obj)
#
#
# session.commit()

# get all tables from the engine
meta = MetaData()
meta.reflect(bind=engine)
tables = meta.tables

from sqlalchemy import text


hm_table_obj = tables['test_pg']

json_column_fields = (
    "details->>'customerId'",
    "details->>'appType'",
    "details->>'vmProtectionGroupType'",
    "details->>'assetsCategory'",
    "details->>'nativeAppInfo'"
    #"details->'nativeAppInfo'->'type'"
)

group_by_columns = [text(c) for c in json_column_fields]
select_columns = []
select_columns.extend(group_by_columns)
select_columns.append(func.count(hm_table_obj.c.id))

print(f'....................group_by_columns: {group_by_columns}')
print(f'....................select_columns: {select_columns}')

select_query = select(select_columns).where(not_(hm_table_obj.c.deleted)).group_by(*group_by_columns)

conn = engine.connect()
result = conn.execute(select_query)
print(f'....................execute_result: {result}')
employment_details = dict()
cust_id_hm_count = {}
for _row in result:
    print(f'...................._row: {_row}')
    cust_id = _row[0]
    app_type = _row[1]
    pg_type = _row[2]
    asset_category = _row[3]
    native_app_info = _row[4]
    if native_app_info :
        print(f'native_app_info: {native_app_info}, type: {type(native_app_info)}')
        native_app_info_dict = json.loads(native_app_info)
        print(f'native_app_info_dict: {native_app_info_dict}, type: {type(native_app_info_dict)}')
    count = _row[5]
    if cust_id in cust_id_hm_count:
        cust_id_hm_count[cust_id] += count
    else:
        cust_id_hm_count[cust_id] = count

print(cust_id_hm_count)


"""
datum=# 
datum=# select * from test_pg;
-[ RECORD 1 ]--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 1
customer_id | cust1
details     | {"customerId": "cust1", "name": "pg1", "appType": "VMware", "vmProtectionGroupType": "Custom", "assetsCategory": "VvolVms"}
deleted     | f
-[ RECORD 2 ]--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 2
customer_id | cust1
details     | {"customerId": "cust1", "name": "pg2", "appType": "VMware", "vmProtectionGroupType": "Custom", "assetsCategory": "VmfsVms"}
deleted     | f
-[ RECORD 3 ]--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 3
customer_id | cust2
details     | {"customerId": "cust2", "name": "pg3", "appType": "VMware", "vmProtectionGroupType": "Native", "nativeAppInfo": {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}}
deleted     | f
-[ RECORD 4 ]--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 4
customer_id | cust2
details     | {"customerId": "cust2", "name": "pg4", "appType": "VMware", "vmProtectionGroupType": "Native", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "type": "VMwareVvolContainer"}}
deleted     | f
-[ RECORD 5 ]--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 5
customer_id | cust2
details     | {"customerId": "cust2", "name": "pg5", "appType": "VMware", "vmProtectionGroupType": "Native", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "type": "VMwareVvolContainer"}}
deleted     | f



datum=# select details->>'nativeAppInfo' as native_type from test_pg group by details->>'customerId',  details->>'nativeAppInfo';
                                            native_type
----------------------------------------------------------------------------------------------------
 {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "type": "VMwareVvolContainer"}
 {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "type": "VMwareVvolContainer"}
 {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}

(4 rows)

datum=#


datum=#  select details->'nativeAppInfo'->'type' as native_type from test_pg;                                                        native_type
-----------------------


 "VMwareFolder"
 "VMwareVvolContainer"
 "VMwareVvolContainer"
(5 rows)

datum=#

datum=#



atlas_virtualization=# select details->>'customerId' as cust_id, details->>'appType' as type, details->>'vmProtectionGroupType' as pg_type, details->>'assetsCategory' as asset_category, details->'nativeAppInfo'->'type' as native_app_info, count(id) from vm_protection_groups where deleted=false group by details->>'customerId', details->>'appType', details->>'vmProtectionGroupType', details->>'assetsCategory', details->'nativeAppInfo'->'type';
             cust_id              |  type  | pg_type | asset_category |    native_app_info    | count
----------------------------------+--------+---------+----------------+-----------------------+-------
 8922afa6723011ebbe01ca32d32b6b77 | VMware | Custom  | VmfsVms        |                       |     1
 8922afa6723011ebbe01ca32d32b6b77 | VMware | Custom  | VvolVms        |                       |     3
 8922afa6723011ebbe01ca32d32b6b77 | VMware | Native  |                | "VMwareFolder"        |     2
 8922afa6723011ebbe01ca32d32b6b77 | VMware | Native  |                | "VMwareVvolContainer" |     2
(4 rows)

atlas_virtualization=#


[root@Aafak-Local-CD-DO-May18 aafak]# python3 group_by_nested_jsonb_col.py
Engine(postgresql://datum:***@127.0.0.1/datum)
....................group_by_columns: [<sqlalchemy.sql.elements.TextClause object at 0x7fc976ba0898>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e972b00>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e972ac8>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e972668>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e047748>]
....................select_columns: [<sqlalchemy.sql.elements.TextClause object at 0x7fc976ba0898>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e972b00>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e972ac8>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e972668>, <sqlalchemy.sql.elements.TextClause object at 0x7fc96e047748>, <sqlalchemy.sql.functions.count at 0x7fc96e04c978; count>]
....................execute_result: <sqlalchemy.engine.result.ResultProxy object at 0x7fc96e04c550>
...................._row: ('cust1', 'VMware', 'Custom', 'VmfsVms', None, 1)
...................._row: ('cust1', 'VMware', 'Custom', 'VvolVms', None, 1)
...................._row: ('cust2', 'VMware', 'Native', None, '{"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}', 1)
native_app_info: {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}, type: <class 'str'>
native_app_info_dict: {'id': 'group-v3312', 'name': 'small-vms', 'type': 'VMwareFolder'}, type: <class 'dict'>
...................._row: ('cust2', 'VMware', 'Native', None, '{"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "type": "VMwareVvolContainer"}', 1)
native_app_info: {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "type": "VMwareVvolContainer"}, type: <class 'str'>
native_app_info_dict: {'id': 'bd714fad-0083-579f-85b8-ee0c08ce8f16', 'name': 'small-vms', 'type': 'VMwareVvolContainer'}, type: <class 'dict'>
...................._row: ('cust2', 'VMware', 'Native', None, '{"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "type": "VMwareVvolContainer"}', 1)
native_app_info: {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "type": "VMwareVvolContainer"}, type: <class 'str'>
native_app_info_dict: {'id': 'bd714fad-0083-579f-85b8-ee0c08ce8f17', 'name': 'small-vms', 'type': 'VMwareVvolContainer'}, type: <class 'dict'>
{'cust1': 2, 'cust2': 3}
You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#

"""