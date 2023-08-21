from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=Engine)
Base = declarative_base()
