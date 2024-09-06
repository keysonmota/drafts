import sqlalchemy

from sqlalchemy.engine.base import Connection

class InjectorFactory:

    _db_connection: Connection

    def __enter__(self):
        from settings import (
            DB_HOST,
            DB_PASS,
            DB_PORT,
            DB_BASE,
            DB_USER
        )

        database_conn_url = f'postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_BASE}'

        # Creating database connection pool
        engine = sqlalchemy.create_engine(
            database_conn_url,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800
        )

        self._db_connection = engine.connect()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_connection.close()

    def db_adapter2(self):
        from nsj_gcf_utils.db_adapter2 import DBAdapter2
        return DBAdapter2(self._db_connection)


    def db_adapter3(self):
        from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
        return DBAdapter3(self._db_connection)


    # def database_dao(self):
    #     from dao.database_dao import DatabaseDAO
    #     return DatabaseDAO(self.db_adapter2())


    # def lock_dao(self):
    #     from dao.lock_dao import LockDAO
    #     return LockDAO(self.db_adapter3())