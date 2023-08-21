from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import func, select

from sqlalchemy.orm import (
    sessionmaker,
    scoped_session)

DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'

engine = create_engine(DB_CONN_URL)
print(engine)

Base = declarative_base()


class HypervisorManager(Base):
    __tablename__ = 'test_hm'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String)
    details = Column(JSON)
    deleted = Column(Boolean)

    def __init__(self, details, deleted):
        self.details = details
        self.deleted = deleted

    def __str__(self):
        return 'User: id:{0}, customer_id:{1}, details: {2}'.format(self.id, self.details)



"""Uncomment following to create the table"""
# Base.metadata.create_all(bind=engine)
# print(f'Created the table')

session = scoped_session(sessionmaker(bind=engine))

hms = [
    ({"customerId": "cust1", "name": "vc1", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.5"},),
    ({"customerId": "cust2", "name": "vc2", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.5"},),
    ({"customerId": "cust2", "name": "vc3", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.5"},),

    ({"customerId": "cust3", "name": "vc4", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.7"},),
    ({"customerId": "cust3", "name": "vc5", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.7"},),
    ({"customerId": "cust3", "name": "vc6", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.7"},),

    ({"customerId": "cust1", "name": "vc7", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.5"},),
    ({"customerId": "cust2", "name": "vc8", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.5"},),
    ({"customerId": "cust2", "name": "vc9", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.5"},),

    ({"customerId": "cust3", "name": "vc10", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.7"},),
    ({"customerId": "cust3", "name": "vc11", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.7"},),
    ({"customerId": "cust3", "name": "vc12", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.7"},)

]


# for e in hms:
#     hm = HypervisorManager(e[0],  False)
#     session.add(hm)
#
#
# session.commit()

# get all tables from the engine
meta = MetaData()
meta.reflect(bind=engine)
tables = meta.tables

from sqlalchemy import text


text("details->['releaseVersion']")
hm_table_obj = tables['test_hm']

select_query = select([text("details->>'customerId'"), text("details->>'hypervisorManagerType'"),  text("details->>'releaseVersion'"), func.count(text("details->>'customerId'"))]
                      ).where(not_(hm_table_obj.c.deleted)).group_by(text("details->>'customerId'"), text("details->>'hypervisorManagerType'"),  text("details->>'releaseVersion'"))

conn = engine.connect()
result = conn.execute(select_query)
print(f'....................execute_result: {result}')
employment_details = dict()
cust_id_hm_count = {}
for _row in result:
    print(f'...................._row: {_row}')
    cust_id = _row[0]
    count = _row[3]
    if cust_id in cust_id_hm_count:
        cust_id_hm_count[cust_id] += count
    else:
        cust_id_hm_count[cust_id] = count

print(cust_id_hm_count)


"""
datum=# select * from test_hm;
 id | customer_id |                                                  details                                                  |
 deleted
----+-------------+-----------------------------------------------------------------------------------------------------------+
---------
  1 |             | {"customerId": "cust1", "name": "vc1", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.5"} |
 f
  2 |             | {"customerId": "cust2", "name": "vc2", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.5"} |
 f
  3 |             | {"customerId": "cust2", "name": "vc3", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.5"} |
 f
  4 |             | {"customerId": "cust3", "name": "vc4", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.7"} |
 f
  5 |             | {"customerId": "cust3", "name": "vc5", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.7"} |
 f
  6 |             | {"customerId": "cust3", "name": "vc6", "hypervisorManagerType": "VMwarevCenter", "releaseVersion": "6.7"} |
 f
  7 |             | {"customerId": "cust1", "name": "vc7", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.5"}       |
 f
  8 |             | {"customerId": "cust2", "name": "vc8", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.5"}       |
 f
  9 |             | {"customerId": "cust2", "name": "vc9", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.5"}       |
 f
 10 |             | {"customerId": "cust3", "name": "vc10", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.7"}      |
 f
 11 |             | {"customerId": "cust3", "name": "vc11", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.7"}      |
 f
 12 |             | {"customerId": "cust3", "name": "vc12", "hypervisorManagerType": "hyper-v", "releaseVersion": "6.7"}      |
 f
(12 rows)

datum=# select details->>'customerId' as cust_id, details->>'hypervisorManagerType' as type, details->>'releaseVersion' as version, count(*) from test_hm group by details->>'customerId', details->>'hypervisorManagerType', details->>'releaseVersion';
 cust_id |     type      | version | count
---------+---------------+---------+-------
 cust2   | VMwarevCenter | 6.5     |     2
 cust3   | hyper-v       | 6.7     |     3
 cust1   | VMwarevCenter | 6.5     |     1
 cust1   | hyper-v       | 6.5     |     1
 cust2   | hyper-v       | 6.5     |     2
 cust3   | VMwarevCenter | 6.7     |     3
(6 rows)

datum=#


[root@Aafak-Local-CD-DO-May18 aafak]# python3 group_by_jsonb_col2.py
Engine(postgresql://datum:***@127.0.0.1/datum)
....................execute_result: <sqlalchemy.engine.result.ResultProxy object at 0x7fd25cd01a58>
...................._row: ('cust2', 'VMwarevCenter', '6.5', 2)
...................._row: ('cust3', 'hyper-v', '6.7', 3)
...................._row: ('cust1', 'VMwarevCenter', '6.5', 1)
...................._row: ('cust1', 'hyper-v', '6.5', 1)
...................._row: ('cust2', 'hyper-v', '6.5', 2)
...................._row: ('cust3', 'VMwarevCenter', '6.7', 3)
{'cust2': 4, 'cust3': 6, 'cust1': 2}

You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#



"""