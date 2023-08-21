from sqlalchemy import create_engine, MetaData, select, text, func, insert, update, delete
from sqlalchemy.engine.url import URL
from app.sqlalchemey_exp.db_crud import constants
from app.sqlalchemey_exp.db_crud import initialize_db


class DBHelper:
    def __init__(self, db_config):
        self.__db_config = db_config
        self.__create_engine()
        meta = MetaData()
        meta.reflect(bind=self.__engine)
        self.__tables = meta.tables

    def __create_engine(self):
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

    def insert_record(self, table, values):
        table_obj = self.__tables[table]
        ins_query = insert(table_obj)
        with self.__engine.connect() as conn:
            conn.execute(ins_query, values)

    def delete_record(self, table, record_id):
        table_obj = self.__tables[table]
        del_query = delete(table_obj).where(table_obj.c.id == record_id)
        with self.__engine.connect() as conn:
            conn.execute(del_query)

    def delete_all_records(self, table):
        print(f'Deleting all the records from the table: {table_name}')
        records = self.get_records(table)
        for record in records:
            self.delete_record(table, record['id'])

    def update_record(self, table, record_id, values):
        table_obj = self.__tables[table]
        update_query = update(table_obj).where(table_obj.c.id == record_id).values(values)
        with self.__engine.connect() as conn:
            conn.execute(update_query, values)


if __name__ == '__main__':
    # initialize_db.initialize(constants.DB_CONFIG)
    table_name = constants.TABLE_BACKUPS
    db_helper = DBHelper(constants.DB_CONFIG)
    # db_helper.delete_all_records(table_name)
    # db_helper.insert_record(table_name, {"name": "Bkp1", "backup_type": "Snapshot"})
    # db_helper.insert_record(table_name, {"name": "Bkp2", "backup_type": "Snapshot"})
    # db_helper.insert_record(table_name, {"name": "Bkp3", "backup_type": "Snapshot"})
    # db_helper.insert_record(table_name, {"name": "Bkp4", "backup_type": "LocalBackup"})
    # db_helper.insert_record(table_name, {"name": "Bkp5", "backup_type": "LocalBackup"})
    # db_helper.insert_record(table_name, {"name": "Bkp6", "backup_type": "LocalBackup"})
    # db_helper.insert_record(table_name, {"name": "Bkp7", "backup_type": "LocalBackup"})
    # db_helper.insert_record(table_name, {"name": "Bkp8", "backup_type": "CloudBackup"})
    # db_helper.insert_record(table_name, {"name": "Bkp9", "backup_type": "CloudBackup"})

    db_helper.get_records(table_name, offset=2, limit=2)
    # db_helper.get_record(table_name, 2)
    # db_helper.update_record(table_name, 2, {"name": "Bkp222"})
    # db_helper.get_records_group_by_columns(table_name, ['backup_type'])  # [('CloudBackup', 2), ('Snapshot', 3), ('LocalBackup', 4)]
    # # delete_record(table_name, 1)
    # db_helper.get_records(table_name)   # [{'id': 2, 'name': 'Bkp2'}]