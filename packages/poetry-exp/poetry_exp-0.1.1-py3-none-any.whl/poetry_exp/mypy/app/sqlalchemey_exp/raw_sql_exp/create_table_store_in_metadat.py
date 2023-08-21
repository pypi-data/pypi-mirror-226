from sqlalchemy import create_engine, Table, Integer, Column, String, inspect
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL


sqlite_db = {
    'drivername': 'sqlite',
    'database': 'dbs//test_create_table'
}
engine = create_engine(URL(**sqlite_db))
meta_data = MetaData(engine)

t1 = Table('Emp', meta_data,
           Column('id', Integer, primary_key=True),
           Column('name', String(255))
     )

# create specific table
#t1.create()

t2 = Table('Person', meta_data,
            Column('id', Integer, primary_key=True),
            Column('name', String(255))
     )

t3 = Table('Student', meta_data,
           Column('id', Integer, primary_key=True),
           Column('name', String(255))
     )

# create all table
meta_data.create_all()

ins = inspect(engine)

print (ins.get_table_names())

# Drop tables
t1.drop(engine)
t2.drop(engine)
t3.drop(engine)
ins = inspect(engine)
print (ins.get_table_names())


"""
[u'Emp', u'Person', u'Student']
[]

"""