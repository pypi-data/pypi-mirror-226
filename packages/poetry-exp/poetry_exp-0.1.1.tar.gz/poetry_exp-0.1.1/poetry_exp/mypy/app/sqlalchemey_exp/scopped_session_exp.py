"""


"""
from sqlalchemy import create_engine, Integer, String, Column, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

sqllite_db = {
    'drivername': 'sqlite',
    'database': 'dbs\\multiplw_session_exp'
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

s_session = scoped_session(sessionmaker(bind=engine))
session1 = s_session()
session2 = s_session()


# Insert
u1 = User('u1')
# In the same session, same object can be added multiple times, no error, but will add only one
session1.add(u1)
session1.add(u1)
session1.commit()

query = session1.query(User).filter()
for user in query.all():
    print (user)

# Same object cannot be added to multiple session
u2 = User('u1')
session1.add(u2)
session2.add(u2)
# No such following error
#sqlalchemy.exc.InvalidRequestError: Object '<User at 0x3f90cf8>' is already attached to session '1' (this is '2')

# But this is permitted in scopped session

"""
If the session objects are retrieved from a scoped_session object,
 however, then we dont have such an issue since the 
 scoped_session object maintains a registry for the same session object

"""

# we can add multiple object at once
session1.add_all([User('u3'), User('u4'), User('u5')])
session1.commit()
query = session1.query(User).filter()
for user in query.all():
    print (user)