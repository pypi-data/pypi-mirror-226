from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_, and_, JSON, Text, cast
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import create_engine
from sqlalchemy import func, select
import json
from sqlalchemy import text


from sqlalchemy.orm import (
    sessionmaker,
    scoped_session)

# https://riptutorial.com/postgresql/example/5195/using-jsonb-operators
DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'

engine = create_engine(DB_CONN_URL)
print(engine)

Base = declarative_base()


class ProtectionGroups(Base):
    __tablename__ = 'test_pg2'
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
    ("cust1", {"assets": [{"id": "vm1", "name": "TEstVM1"},{"id": "vm2", "name": "TEstVM2"}],"customerId": "cust1", "name": "pg1", "appType": "VMware", "vmProtectionGroupType": "Custom",
      "assetsCategory": "VvolVms", "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False),
    ("cust1", {"assets": [{"id": "vm1", "name": "TEstVM1"},{"id": "vm3", "name": "TEstVM3"}],"customerId": "cust1", "name": "pg2", "appType": "VMware", "vmProtectionGroupType": "Custom",
      "assetsCategory": "VmfsVms", "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False),

    ("cust1", {"assets": [{"id": "vm1", "name": "TEstVM1"},{"id": "vm4", "name": "TEstVM4"}],"customerId": "cust1", "name": "pg3", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}, "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, True),

    ("cust2", {"assets": [{"id": "vm2", "name": "TEstVM1"},{"id": "vm6", "name": "TEstVM6"}],"customerId": "cust2", "name": "pg4", "appType": "VMware", "vmProtectionGroupType": "Native",
      "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms",
                        "type": "VMwareVvolContainer"}, "hypervisorManagerInfo":
          {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094",
           "name": "172.17.29.162", "displayName": "Aafak-vCenter"}}, False),

    ("cust3", {"assets": [{"id": "vm1", "name": "TEstVM1"},{"id": "vm2", "name": "TEstVM2"}],"customerId": "cust3", "name": "pg5", "appType": "VMware", "vmProtectionGroupType": "Native",
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


hm_table_obj = tables['test_pg2']

json_column_fields = (
    "details->'hypervisorManagerInfo'->'id'"
)

select_column_fields = (
    "details->>'customerId'",
    "details->>'name'",
    "details->>'assets'",
)
select_columns = [text(c) for c in select_column_fields]
where_columns = [text(c) for c in json_column_fields]

"""
SELECT * FROM test_pg2 WHERE (details->'assets' @> '[{"id": "vm1"}]');

SELECT id FROM test_pg2 WHERE (details->'assets' @> '[{"id": "vm1"}]');

"""

vm_id = "vm2"
cust_id = "cust1"
select_query = "SELECT * FROM test_pg2 WHERE (details->" +\
               "'assets' @> '[{" + "\"id\":" + "\"" + vm_id + "\"}]') and customer_id='" + cust_id + "' and deleted=false;"
conn = engine.connect()
result = conn.execute(select_query)
print(f'....................execute_result: {result}')
employment_details = dict()
for _row in result:
    print(f'...................._row: {_row}')
    cust_id = _row[0]
    app_type = _row[1]



"""
datum=# select * from test_pg2;
 id | customer_id |
                                                                                                       details

                                                                      | deleted
----+-------------+---------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------+---------
  1 | cust1       | {"name": "pg1", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appType
": "VMware", "customerId": "cust1", "assetsCategory": "VvolVms", "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5
bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Custom"}
                                                                      | f
  2 | cust1       | {"name": "pg2", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm3", "name": "TEstVM3"}], "appType
": "VMware", "customerId": "cust1", "assetsCategory": "VmfsVms", "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5
bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Custom"}
                                                                      | f
  3 | cust1       | {"name": "pg3", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm4", "name": "TEstVM4"}], "appType
": "VMware", "customerId": "cust1", "nativeAppInfo": {"id": "group-v3312", "name": "small-vms", "type": "VMwareFolder"}, "hy
pervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"
}, "vmProtectionGroupType": "Native"}                                 | t
  4 | cust2       | {"name": "pg4", "assets": [{"id": "vm2", "name": "TEstVM1"}, {"id": "vm6", "name": "TEstVM6"}], "appType
": "VMware", "customerId": "cust2", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
  5 | cust3       | {"name": "pg5", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appType
": "VMware", "customerId": "cust3", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
(5 rows)

datum=# SELECT * FROM test_pg2 WHERE (details->'assets' @> '[{"id": "vm2"}]');
 id | customer_id |
                                                                                                       details

                                                                      | deleted
----+-------------+---------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------+---------
  1 | cust1       | {"name": "pg1", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appType
": "VMware", "customerId": "cust1", "assetsCategory": "VvolVms", "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5
bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Custom"}
                                                                      | f
  4 | cust2       | {"name": "pg4", "assets": [{"id": "vm2", "name": "TEstVM1"}, {"id": "vm6", "name": "TEstVM6"}], "appType
": "VMware", "customerId": "cust2", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
  5 | cust3       | {"name": "pg5", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appType
": "VMware", "customerId": "cust3", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
(3 rows)

datum=#

"""
