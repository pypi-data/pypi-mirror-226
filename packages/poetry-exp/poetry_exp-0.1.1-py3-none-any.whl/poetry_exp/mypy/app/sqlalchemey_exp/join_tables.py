from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id    = Column(Integer, primary_key=True)
    name  = Column(String)
    addresses = relationship("Address", backref="user")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

db_url = {'drivername': 'sqlite',
          'database': 'dbs//join_exp',
         }

# create engine
engine = create_engine(URL(**db_url))

# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

user = User(name='user1')
mail1 = Address(email='user1@foo.com')
mail2 = Address(email='user1@bar.com')
user.addresses.extend([mail1, mail2])

user2 = User(name='user2')
mail3 = Address(email='user2@foo.com')
mail4 = Address(email='user2@bar.com')
user2.addresses.extend([mail3, mail4])

session.add_all([user, user2])
session.add_all([mail1, mail2, mail3, mail4])
session.commit()

query = session.query(Address, User).join(User)
for _a, _u in query.all():
    print(_u.name, _a.email, _a.user_id)