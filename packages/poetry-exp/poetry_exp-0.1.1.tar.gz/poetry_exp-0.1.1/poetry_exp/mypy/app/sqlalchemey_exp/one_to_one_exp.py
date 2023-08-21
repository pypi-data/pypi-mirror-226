"""
for mysql: pip install pymysql

pymysql is driver for mysql
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child = relationship("Child", uselist=False, back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="child")

"""


from sqlalchemy import create_engine, Column, Integer, ForeignKey, BLOB, String
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

#Engine = create_engine("sqlite:///dbs//one_to_one_exp.db")
Engine = create_engine("mysql+pymysql://root:test@localhost:3306/cloud", echo=True)
Session = scoped_session(sessionmaker(bind=Engine, autocommit=True, autoflush=True))
Base = declarative_base()

# Models


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    aadhar = relationship("Aadhar", uselist=False, back_populates="person")

    def __init__(self, name):
        self.name = name


class Aadhar(Base):
    __tablename__ = 'aadhar'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"))
    fingure_print = Column(String(30))
    person = relationship("Person", back_populates="aadhar")

    def __init__(self, person_id, fingure_print):
        self.person_id = person_id
        self.fingure_print = fingure_print

# Note: Delete the existing Db if modify the Models

if __name__ == '__main__':
    Base.metadata.create_all(Engine)

    # p1 = Person('Aafak')
    # Session.add(p1)
    # person = Session.query(Person).filter(Person.name == 'Aafak').first()
    # print 'Person with name:', person.name, ' saved'
    #
    # a1 = Aadhar(person.id, "fp")
    # Session.add(a1)
    # aadhar = Session.query(Aadhar).filter().first()
    # print 'Saved successfully, Aadhar ID:', aadhar.id, aadhar.person.name
    #
    # person = Session.query(Person).filter(Person.name == 'Aafak').first()
    # print person
    # print person.aadhar.id

