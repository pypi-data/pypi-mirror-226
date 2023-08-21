# https://github.com/crazyguitar/pysheeet/blob/master/docs/notes/python-sqlalchemy.rst

from sqlalchemy import create_engine
from sqlalchemy import inspect

db_uri = 'sqlite:///dbs//meta_data.db'
engine = create_engine(db_uri)

inspector = inspect(engine)

# Get table information
print(inspector.get_table_names())

# Get column information
print(inspector.get_columns('Example'))


"""
[u'Example']
[{'primary_key': 1, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'id'},
 {'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(), 'name': u'name'}]

"""