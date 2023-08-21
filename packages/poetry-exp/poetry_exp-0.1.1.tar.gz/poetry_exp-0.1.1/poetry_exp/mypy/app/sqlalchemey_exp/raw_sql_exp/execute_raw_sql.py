
from sqlalchemy import create_engine, Column, Integer, ForeignKey, BLOB, String
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

#Engine = create_engine("sqlite:///dbs//one_to_one_exp.db")
Engine = create_engine("mysql+pymysql://root:test@localhost:3306/cloud", echo=True)

result = Engine.execute("select * from person")
for p in result.fetchall():
    print (f'...............{p}')