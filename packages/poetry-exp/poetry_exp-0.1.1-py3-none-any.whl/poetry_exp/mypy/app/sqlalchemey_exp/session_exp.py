"""
Session maintains all the conversation between python app and database
# sessionmaker is factory method to create session

Session Object States:
Transient: an instance that's not included in a session and has not been persisted to the database.
Pending: an instance that has been added to a session but not persisted to a database yet.
        It will be persisted to the database in the next session.commit().
Persistent: an instance that has been persisted to the database and also included in a session.
           You can make a model object persistent by committing it to the database or query it from the database.
Detached: an instance that has been persisted to the database but not included in any sessions.

Let's use sqlalchemy.inspect to take a look at the states of a new User object david.
"""

from sqlalchemy import create_engine, Integer, String, Column, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

sqllite_db = {
    'drivername': 'sqlite',
    'database': 'dbs\\session_exp'
}

engine = create_engine(URL(**sqllite_db))

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'User: id:{0}, name:{1}'.format(self.id, self.name)


Base.metadata.create_all(engine)

session1 = sessionmaker(bind=engine)()

# Insert
u1 = User('u1')
insp = inspect(u1)
print (insp.transient) # True
session1.add(u1)
print (insp.pending) # True
session1.commit()
print (insp.persistent) # True

# Fetch
query = session1.query(User).filter(User.id==2)
user = query.first()
print (user) # User: id:1, name:u1

# update
user.name = 'u2'
session1.add(user)
session1.commit()

# Fetch
query = session1.query(User).filter(User.id==2)
user = query.first()
print (user) # User: id:1, name:u2

# Delete
session1.delete(user)
session1.commit()

# Fetch
query = session1.query(User).filter(User.id==2)
user = query.first()
print (user) # None

session1.close()
print (insp.detached)  # True




