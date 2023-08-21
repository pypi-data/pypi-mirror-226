"""
you could use this to create a database session and close it after finishing.

Only the code prior to and including the yield statement is executed before sending a response:

The code following the yield statement is executed after the response has been delivered:


"""


from fastapi import FastAPI, APIRouter, status, Depends
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import uvicorn
import os

DB_CONFIG = {
            'drivername': 'sqlite',
            'database': 'fast_api_exp.db'
        }
ENGINE = create_engine(URL(**DB_CONFIG))

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'User: id:{0}, name:{1}'.format(self.id, self.name)


def get_db_session():
    session = None
    try:
        session = sessionmaker(bind=ENGINE)()
        yield session  # FastAPI dependencies with yield require Python 3.7 or above,
    finally:
        if session:
            print(f'Closing the session')
            session.close()


def get_db_session2():
    session = sessionmaker(bind=ENGINE)()
    return session


def initialize_db():
    db_file_path = DB_CONFIG['database']
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
    Base.metadata.create_all(bind=ENGINE)
    session = get_db_session2()
    for i in range(1, 11):
        session.add(User("user-" + str(i)))
    session.commit()


router = APIRouter()


@router.get("/users")
async def get_users(db_session=Depends(get_db_session2)):
    users = db_session.query(User).all()
    print(f'Users: {users}')
    return users

if __name__ == '__main__':
    initialize_db()
    app = FastAPI()
    app.include_router(router, prefix="/api/v1", tags=["Test dependency injection with yield"])
    uvicorn.run(app)



