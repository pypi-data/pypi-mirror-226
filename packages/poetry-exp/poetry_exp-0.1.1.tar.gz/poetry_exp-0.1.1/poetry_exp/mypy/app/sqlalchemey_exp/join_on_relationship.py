from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    func)

from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

db_url = {'drivername': 'sqlite',
          'database': 'dbs//join_exp',
         }

# create engine
engine = create_engine(URL(**db_url))

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id       = Column(Integer, primary_key=True)
    name     = Column(String)
    children = relationship('Child', back_populates='parent')

class Child(Base):
    __tablename__ = 'child'
    id        = Column(Integer, primary_key=True)
    name      = Column(String)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent    = relationship('Parent', back_populates='children')

Base.metadata.create_all(bind=engine)
Session = scoped_session(sessionmaker(bind=engine))

p1 = Parent(name="Alice")
p2 = Parent(name="Bob")

c1 = Child(name="foo")
c2 = Child(name="bar")
c3 = Child(name="ker")
c4 = Child(name="cat")

p1.children.extend([c1, c2, c3])
p2.children.append(c4)

try:
    Session.add(p1)
    Session.add(p2)
    Session.commit()

    # count number of children
    q = Session.query(Parent, func.count(Child.id))\
               .join(Child)\
               .group_by(Parent.id)

    # print result
    for _p, _c in q.all():
        print('parent: {}, num_child: {}'.format(_p.name, _c))
finally:
    Session.remove()