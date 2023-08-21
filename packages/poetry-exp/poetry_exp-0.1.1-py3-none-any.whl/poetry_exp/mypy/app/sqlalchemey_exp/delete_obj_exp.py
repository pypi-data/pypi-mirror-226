
from sqlalchemy import create_engine, Integer, String, Column, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

sqllite_db = {
    'drivername': 'sqlite',
    'database': 'dbs\\delete_exp'
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
session1.add(u1)
session1.commit()

# Fetch
query = session1.query(User).filter(User.id == 1)
print query.first() # User: id:1, name:u1
query.delete()
session1.commit()
session1.close()


session1 = sessionmaker(bind=engine)()
# Fetch
query = session1.query(User).filter(User.id==1)
print query.first() # None