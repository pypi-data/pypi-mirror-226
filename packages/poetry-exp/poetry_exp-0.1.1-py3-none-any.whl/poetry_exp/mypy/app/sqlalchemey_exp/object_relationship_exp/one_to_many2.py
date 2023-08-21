from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

Base = declarative_base()

sqllite_db = {
    'drivername': 'sqlite',
    'database': 'dbs\\one_to_many2'
}

engine = create_engine(URL(**sqllite_db))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    addresses = relationship("Address", backref="user")

    def __init__(self, name):
        self.name = name


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email


Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

u1 = User('u1')
session.add(u1)
session.commit()

user = session.query(User).filter(User.name == 'u1').first()
a1 = Address(user.id, 'abc@yahoo.com')
a2 = Address(user.id, 'abc@yahoo.com')
session.add(a1)
session.add(a2)

user = session.query(User).filter(User.name == 'u1').first()
print (user.addresses)
