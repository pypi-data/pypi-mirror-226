"""
many to one: Many to one places a foreign key in the parent table referencing the child. relationship() is declared on the parent, where a new scalar-holding attribute will be created:

Many states belongs to one Country
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-one
"""