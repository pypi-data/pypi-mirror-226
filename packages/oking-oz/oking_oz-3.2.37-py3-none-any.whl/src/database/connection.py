import mysql.connector
import cx_Oracle
import pyodbc

from src.database.utils import DatabaseConfig
import src


class Connection:
    def __init__(self, db_config: DatabaseConfig):
        self.db_type = db_config.db_type.lower()
        self.db_config = db_config
        if self.db_type == 'mysql':
            self.conn = get_mysql_connection(db_config.db_host, db_config.db_name, db_config.db_user, db_config.db_pwd, db_config.port)
        elif self.db_type == 'oracle':
            self.conn = get_oracle_client_connection(db_config.db_client, db_config.db_user, db_config.db_pwd, db_config.db_host)
        elif self.db_type == 'sql':
            self.conn = get_sql_server_connection(db_config.db_client, db_config.db_host, db_config.db_name, db_config.db_user, db_config.db_pwd)

    def get_conect(self):
        if self.db_type == 'oracle':
            return get_oracle_connection(self.db_config.db_host, self.db_config.db_user, self.db_config.db_pwd)
        else:
            return self.conn


def get_mysql_connection(db_host: str, db_name: str, db_user: str, db_pwd: str, db_port: str = '3306'):
    if db_port is None or db_port == '':
        db_port = '3306'

    return mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pwd,
        port=db_port)


def get_oracle_connection(db_host: str, db_user: str, db_pwd):
    conn_str = db_user + '/' + db_pwd + '@' + db_host
    return cx_Oracle.connect(conn_str)


def get_oracle_client_connection(db_client: str, db_user: str, db_pwd: str, db_host: str):
    if src.is_connected_oracle_client is False:
        cx_Oracle.init_oracle_client(lib_dir=rf'{db_client}')
        src.is_connected_oracle_client = True

    return cx_Oracle.connect(user=db_user,
                             password=db_pwd,
                             dsn=db_host)


def get_sql_server_connection(db_driver: str, db_host: str, db_name: str, db_user:str, db_pwd: str):
    return pyodbc.connect(f'Driver={{{db_driver}}};Server={db_host};Database={db_name};UID={db_user};PWD={db_pwd}')


def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
    if default_type == cx_Oracle.DB_TYPE_BLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)
