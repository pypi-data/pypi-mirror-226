
from sqlalchemy import create_engine, Integer, String, Column, inspect
from sqlalchemy.orm import sessionmaker
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

session = sessionmaker()
session.configure(bind=engine)
session1 = session()


session2 = sessionmaker()
session2.configure(bind=engine)
session2 = session2()

"""
If you call sessionmaker() a second time, you will get a new session object whose
 states are independent of the previous session
"""

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
# u2 = User('u1')
# session1.add(u2)
# session2.add(u2)
#sqlalchemy.exc.InvalidRequestError: Object '<User at 0x3f90cf8>' is already attached to session '1' (this is '2')

# But this is permitted in scopped session