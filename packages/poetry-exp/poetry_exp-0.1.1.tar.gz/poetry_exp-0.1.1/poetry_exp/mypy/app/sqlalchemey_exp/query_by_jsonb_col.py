from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_, and_, JSON, Text, cast
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

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
    details = Column(JSONB)
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
    ("cust1", {"customerId": "cust1", "name": "pg1", "appType": "VMware", "vmProtectionGroupType": "Custom",
      "assetsCategory": "VvolVms", "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False),
    ("cust1", {"customerId": "cust1", "name": "pg2", "appType": "VMware", "vmProtectionGroupType": "Custom",
      "assetsCategory": "VmfsVms", "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False),

    ("cust1", {"customerId": "cust1", "name": "pg3", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}, "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, True),

    ("cust2", {"customerId": "cust2", "name": "pg4", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms",
                        "type": "VMwareVvolContainer"}, "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False),

    ("cust3", {"customerId": "cust3", "name": "pg5", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms",
                        "type": "VMwareVvolContainer"}, "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False)
]

"""Uncomment following to create the records"""
#
# for pg in protection_groups:
#     print(f"@@@@@@@@@@@@@pg: {pg}")
#     pg_obj = ProtectionGroups(pg[0], pg[1],  pg[2])
#     session.add(pg_obj)
#
# session.commit()

# get all tables from the engine
meta = MetaData()
meta.reflect(bind=engine)
tables = meta.tables

from sqlalchemy import text


hm_table_obj = tables['test_pg']

json_column_fields = (
    "details->'hypervisorManagerInfo'->'id'"
)

select_column_fields = (
    "details->>'appType'",
    "details->>'vmProtectionGroupType'",
    "details->>'hypervisorManagerInfo'",
    "details->>'name'",
    "id",
    "customer_id",
    "deleted"
)

select_column_fields = (
   "details->>'hypervisorManagerInfo'",
   "details->>'name1'",
)
select_columns = [text(c) for c in select_column_fields]
where_columns = [text(c) for c in json_column_fields]

"""
select_query = select(select_columns).where(and_(
    hm_table_obj.c.deleted==False,
    hm_table_obj.c.details["customerId"].astext.like(f'%{2}%')))
        
select_query = select(select_columns).where(and_(
    hm_table_obj.c.deleted==False,
    hm_table_obj.c.details["customerId"].astext=="1"))

 SELECT details  FROM test_pg WHERE details -> 'hypervisorManagerInfo' ->> 'id' = 'd9434f8d-b8a0-44fc-b065-c5bce71a4093';
 
  SELECT id FROM virtual_machines WHERE details -> 'hypervisorManagerInfo' ->> 'id' = '413e5eab-172e-43df-af77-fcadbde34005';

 """

select_query = select(select_columns).where(and_(
    hm_table_obj.c.deleted==False,
    hm_table_obj.c.details["hypervisorManagerInfo"]["id"].astext=="d9434f8d-b8a0-44fc-b065-c5bce71a4093"))

# To select all columns
# select_query = select('*').where(and_(
#     hm_table_obj.c.deleted==False,
#     hm_table_obj.c.details["hypervisorManagerInfo"]["id"].astext=="d9434f8d-b8a0-44fc-b065-c5bce71a4093"))

conn = engine.connect()
result = conn.execute(select_query)
print(f'....................execute_result: {result}')

for _row in result:
    print(f'...................._row: {_row}')
    # cust_id = _row[0]
    # app_type = _row[1]
    # pg_type = _row[2]
    # hm_info = _row[3]


"""
[root@Atlas-DO3 site-packages]# python3.6 query_by_jsonb_col.py
Engine(postgresql://datum:***@127.0.0.1/datum)
....................execute_result: <sqlalchemy.engine.result.ResultProxy object at 0x7f4ea852bd30>
...................._row: ('VMware', 'Custom', '{"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}', 'pg1', 1, 'cust1', False)
...................._row: ('VMware', 'Custom', '{"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}', 'pg2', 2, 'cust1', False)
You have mail in /var/spool/mail/root
[root@Atlas-DO3 site-packages]#

"""

#
# response = [dict(row) for row in result]
# print(response)

"""

[{'id': 1, 'customer_id': 'cust1', 'details': {'name': 'pg1', 'appType': 'VMware', 'customerId': 'cust1', 'assetsCategory': 'VvolVms', 'hypervisorManagerInfo': {'id': 'd9434f8d-b8a0-44fc-b065-c5bce71a4093', 'name': '172.17.29.162', 'displayName': 'Aafak-vCenter'}, 'vmProtectionGroupType': 'Custom'}, 'deleted': False}, {'id': 2, 'customer_id': 'cust1', 'details': {'name': 'pg2', 'appType': 'VMware', 'customerId': 'cust1', 'assetsCategory': 'VmfsVms', 'hypervisorManagerInfo': {'id': 'd9434f8d-b8a0-44fc-b065-c5bce71a4093', 'name': '172.17.29.162', 'displayName': 'Aafak-vCenter'}, 'vmProtectionGroupType': 'Custom'}, 'deleted': False}]


"""
