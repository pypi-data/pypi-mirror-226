from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_, and_, JSON, Text, cast
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import create_engine
from sqlalchemy import func, select, update, bindparam, literal_column
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
    __tablename__ = 'test_pg3'
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


hm_table_obj = tables['test_pg3']

# update test_pg3 set details=jsonb_set(details, '{"name"}', '"pg111"') where id=1;
pg_id = 1
pg_name = "pg1111111111"
customer_id ="cust11111111111"
with engine.connect() as conn:

    # WOrking one1
    # update_query = update(hm_table_obj).where(hm_table_obj.c.id == pg_id).values(
    #         details = literal_column("jsonb_set(details, '{name}','\""+pg_name+"\"')"),
    #         customer_id=customer_id
    #     )

    # Working 2
    # update_data = {
    #     "name": "pg01111",
    #     "appType": "VMware111"
    # }
    # update_query = update(hm_table_obj).where(hm_table_obj.c.id == pg_id).values(
    #     details=hm_table_obj.c.details.op('||')(update_data),
    #     customer_id=customer_id
    # )

    update_values = {
        "details": {
            "name": "pg00111",
            "appType": "VMware000111"
        },
        "customer_id": "cust00111"
    }
    # update_query = update(hm_table_obj).where(hm_table_obj.c.id == pg_id).values(
    #     **{k: v if not isinstance(v, dict) else hm_table_obj.c[k].op('||')(v) for k, v in update_values.items()}
    # )

    values_dict = {
                        k: v if not isinstance(v, dict) else
                        hm_table_obj.c[k].op('||')(v) for k, v in update_values.items()
                  }
    update_query = (
        update(hm_table_obj).where(
            ((hm_table_obj.c.id == pg_id)
             & (hm_table_obj.c.customer_id == customer_id)
             )
        ).values(**values_dict)
    )

    """
    stmt = update(my_table).where(my_table.c.id == 123).values(
        **{k: v if not isinstance(v, dict) else my_table.c[k].op('||')(v) for k, v in column_dict.items()}
    )
    """

    conn.execute(update_query)
    print(f'Updated the records')
    select_query = select('*').where(and_(
        hm_table_obj.c.deleted == False,
        hm_table_obj.c.id == pg_id))
    result = conn.execute(select_query)
    print(f'result: {result}')
    for row in result:
        print(row)



"""
datum=#  SELECT * FROM test_pg3 WHERE (details->'assets' @> '[{"id": "vm2"}]') and deleted=false;
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

datum=#  update test_pg3 set details=jsonb_set(details, '{"name"}', '"pg111"') where id=1;
UPDATE 1
datum=#  SELECT * FROM test_pg2 WHERE (details->'assets' @> '[{"id": "vm2"}]') and deleted=false;
 id | customer_id |
                                                                                                       details

                                                                      | deleted
----+-------------+---------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------+---------
  4 | cust2       | {"name": "pg4", "assets": [{"id": "vm2", "name": "TEstVM1"}, {"id": "vm6", "name": "TEstVM6"}], "appType
": "VMware", "customerId": "cust2", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
  5 | cust3       | {"name": "pg5", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appType
": "VMware", "customerId": "cust3", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
  1 | cust1       | {"name": "pg111", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appTy
pe": "VMware", "customerId": "cust1", "assetsCategory": "VvolVms", "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-
c5bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Custom"}
                                                                      | f
(3 rows)

datum=#

datum=#  update test_pg3 set details=jsonb_set(details, '{"name"}', '"pg1111111"'),customer_id='cust111' where id=1;
UPDATE 1
datum=#  SELECT * FROM test_pg2 WHERE (details->'assets' @> '[{"id": "vm2"}]') and deleted=false;
 id | customer_id |
                                                                                                       details

                                                                      | deleted
----+-------------+---------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------+---------
  4 | cust2       | {"name": "pg4", "assets": [{"id": "vm2", "name": "TEstVM1"}, {"id": "vm6", "name": "TEstVM6"}], "appType
": "VMware", "customerId": "cust2", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f17", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
  5 | cust3       | {"name": "pg5", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "appType
": "VMware", "customerId": "cust3", "nativeAppInfo": {"id": "bd714fad-0083-579f-85b8-ee0c08ce8f16", "name": "small-vms", "ty
pe": "VMwareVvolContainer"}, "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b065-c5bce71a4094", "name": "172.17.29.162"
, "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Native"} | f
  1 | cust111     | {"name": "pg1111111", "assets": [{"id": "vm1", "name": "TEstVM1"}, {"id": "vm2", "name": "TEstVM2"}], "a
ppType": "VMware", "customerId": "cust1", "assetsCategory": "VvolVms", "hypervisorManagerInfo": {"id": "d9434f8d-b8a0-44fc-b
065-c5bce71a4093", "name": "172.17.29.162", "displayName": "Aafak-vCenter"}, "vmProtectionGroupType": "Custom"}
                                                                      | f
(3 rows)

datum=#

"""
