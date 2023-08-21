from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

mysql_db = {
    'drivername': 'mysql+pymysql',
    'username': 'root',
    'password': 'test',
    'host': 'localhost',
    'port': 3306,
    'database': 'cloud'
}

print (URL(**mysql_db))  # pymysql://root:test@localhost:3306
mysql_engine = create_engine(URL(**mysql_db))
result = mysql_engine.execute("select * from person")
print (result.fetchall()) # [(1, 'Asad'), (2, 'Asad2'), (3, 'Ajay'), (4, 'Aafak'), (5, 'Aafak'), (6, 'Aafak')]



sqlite_db = {'drivername': 'sqlite', 'database': 'db.sqlite'}
print (URL(**sqlite_db))  #  sqlite:///db.sqlite
sqlite_engine = create_engine(URL(**sqlite_db))
print (sqlite_engine)  # Engine(sqlite:///db.sqlite)