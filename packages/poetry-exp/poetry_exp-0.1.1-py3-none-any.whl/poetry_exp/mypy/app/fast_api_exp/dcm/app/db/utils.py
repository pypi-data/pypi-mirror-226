from sqlalchemy import create_engine, MetaData, select, text, func, insert, update, delete
from sqlalchemy.engine.url import URL
from app.db.models import Base
from app.db.const import DB_CONN_URL


class DBHelper:
    def __init__(self, db_config=None, db_conn_url=DB_CONN_URL):
        self.__db_config = db_config
        self.db_conn_url = db_conn_url
        self.__create_engine()
        meta = MetaData()
        meta.reflect(bind=self.__engine)
        self.__tables = meta.tables

    def __create_engine(self):
        if self.db_conn_url:
            print(f'Creating engine...with db_conn_url: {self.db_conn_url}')
            self.__engine = create_engine(self.db_conn_url)
            Base.metadata.create_all(bind=self.__engine)
        else:
            print(f'Creating engine...')
            self.__engine = create_engine(URL(**self.__db_config))
        print(f'Engine created successfully')

    def get_records(self, table, offset=0, limit=10):
        table_obj = self.__tables[table]
        sel_query = select([table_obj], offset=offset, limit=limit)
        with self.__engine.connect() as conn:
            result = conn.execute(sel_query)
            result_dict = [dict(_row) for _row in result]
            print(f'Total records: {len(result_dict)}')
            print(result_dict)
            return result_dict

    def get_records_group_by_columns(self, table, columns=[]):
        table_obj = self.__tables[table]
        group_by_cols = [text(col) for col in columns]
        select_cols = []
        select_cols.extend(group_by_cols)
        select_cols.append(func.count(table_obj.c.id))
        sel_query = select(select_cols).group_by(*group_by_cols)
        with self.__engine.connect() as conn:
            result = conn.execute(sel_query)
            results = list(result)
            print(results)
            return results

    def get_record(self, table, record_id):
        table_obj = self.__tables[table]
        sel_query = select([table_obj]).where(table_obj.c.id == record_id)
        with self.__engine.connect() as conn:
            result = conn.execute(sel_query)
            result_dict = [dict(_row) for _row in result]
            print(result_dict)
            return result_dict

    def get_by_username(self, table, username):
        table_obj = self.__tables[table]
        sel_query = select([table_obj]).where(table_obj.c.username == username)
        with self.__engine.connect() as conn:
            result = conn.execute(sel_query)  # result will not be in terms of model object
            result_dict = [dict(_row) for _row in result]
            print(result_dict)
            user = None
            if result:
                user = result_dict[0]
            return user

    def insert_record(self, table, values):
        table_obj = self.__tables[table]
        ins_query = insert(table_obj)
        print(f'Creating record with query: {ins_query}')
        with self.__engine.connect() as conn:
            conn.execute(ins_query, values)
        print('Records inserted successfully..')

    def delete_record(self, table, record_id):
        table_obj = self.__tables[table]
        del_query = delete(table_obj).where(table_obj.c.id == record_id)
        with self.__engine.connect() as conn:
            conn.execute(del_query)

    def delete_all_records(self, table):
        print(f'Deleting all the records from the table: {table}')
        records = self.get_records(table)
        for record in records:
            self.delete_record(table, record['id'])

    def update_record(self, table, record_id, values):
        table_obj = self.__tables[table]
        update_query = update(table_obj).where(table_obj.c.id == record_id).values(values)
        with self.__engine.connect() as conn:
            conn.execute(update_query, values)
