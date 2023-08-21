"""
Many to Many adds an association table between two classes.
The association table is indicated by the secondary argument to relationship().
 Usually, the Table uses the MetaData object associated with the declarative base class,
 so that the ForeignKey directives can locate the remote tables with which to link:
"""


from sqlalchemy import create_engine, Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine("sqlite:///dbs//many_to_many_exp.db")
Session = scoped_session(sessionmaker(bind=Engine, autoflush=True, autocommit=True))
Base = declarative_base()

emp_training_association = Table(
    "emp_training",
    Base.metadata,
    Column('emp_id', Integer, ForeignKey('emp.id')),
    Column('training_id', Integer, ForeignKey('training.id'))

)


class Emp(Base):
    __tablename__ = 'emp'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    training = relationship("Training", secondary=emp_training_association, back_populates="emp")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        trainings = [training.name for training in self.training]
        return "Name: {0}, Trainings: {1}".format(self.name, ", ".join(trainings))


class Training(Base):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    emp = relationship("Emp", secondary=emp_training_association, back_populates="training")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        employees = [e.name for e in self.emp]
        return "Training: {0}, Employees:{1}".format(self.name, ",".join(employees))


if __name__ == '__main__':
    Base.metadata.create_all(Engine)

    e1 = Emp("Aman")
    e2 = Emp("Aakash")
    Session.add(e1)
    Session.add(e2)
    emp1 = Session.query(Emp).filter(Emp.name == 'Aman').first()
    emp2 = Session.query(Emp).filter(Emp.name == 'Aakash').first()
    t1 = Training('java')
    t1.emp = [emp1, emp2]
    t2 = Training('Python')
    t2.emp = [emp1, emp2]
    Session.add(t1)
    Session.add(t2)

    java_train = Session.query(Training).filter(Training.name == 'java').first()
    python_train = Session.query(Training).filter(Training.name == 'Python').first()
    emp1 = Session.query(Emp).filter(Emp.name == 'Aman').first()
    emp2 = Session.query(Emp).filter(Emp.name == 'Aakash').first()

    print (java_train)  # Training: java, Employees:Aman,Aakash
    print (python_train) # Training: Python, Employees:Aman,Aakash
    print (emp1)  # Name: Aman, Trainings: java, Python
    print (emp2)  # Name: Aakash, Trainings: java, Python



