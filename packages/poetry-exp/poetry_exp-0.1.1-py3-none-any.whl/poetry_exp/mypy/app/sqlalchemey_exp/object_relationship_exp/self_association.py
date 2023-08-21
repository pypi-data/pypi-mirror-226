import json

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine,
    Table)

from sqlalchemy.engine.url import URL
from sqlalchemy.orm import (
    sessionmaker,
    relationship)

from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

sqllite_db = {
    'drivername': 'sqlite',
    'database': 'dbs\\one_to_many2'
}

engine = create_engine(URL(**sqllite_db))

association = Table("Association", base.metadata,
    Column('left', Integer, ForeignKey('node.id'), primary_key=True),
    Column('right', Integer, ForeignKey('node.id'), primary_key=True))

class Node(base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    friends = relationship('Node',
                           secondary=association,
                           primaryjoin=id==association.c.left,
                           secondaryjoin=id==association.c.right,
                           backref='left')
    def to_json(self):
        return dict(id=self.id,
                    friends=[_.label for _ in self.friends])

nodes = [Node(label='node_{}'.format(_)) for _ in range(0, 3)]
nodes[0].friends.extend([nodes[1], nodes[2]])
nodes[1].friends.append(nodes[2])

print('----> right')
print(json.dumps([_.to_json() for _ in nodes], indent=2))

print('----> left')
print(json.dumps([_n.to_json() for _n in nodes[1].left], indent=2))