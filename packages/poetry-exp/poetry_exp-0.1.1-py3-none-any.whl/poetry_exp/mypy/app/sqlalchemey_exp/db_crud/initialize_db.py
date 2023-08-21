from app.sqlalchemey_exp.db_crud.models import Base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine


def initialize(db_config, create_if_not_exists=True):
    print(f'Initializing database...')
    engine = create_engine(URL(**db_config))
    Base.metadata.create_all(bind=engine, checkfirst=create_if_not_exists)
    print(f'Successfully initialized database ')
