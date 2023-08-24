from bewe.services.crawler import secret_manager
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
import os


DB_NAME_KEY = 'DB_NAME'
DB_USER_KEY = 'DB_USER'
DB_PASS_KEY = 'DB_PASS'
INSTANCE_KEY = 'DB_INSTANCE'


metadata = sqlalchemy.MetaData()
Stock = sqlalchemy.Table(
    'stock', metadata,
    sqlalchemy.Column('stock_id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('stock_name', sqlalchemy.String)
)


class DBManager:
    def __init__(self):
        self.instance = secret_manager.get_secret_tokens(INSTANCE_KEY)
        self.engine = sqlalchemy.create_engine(
            'mysql+pymysql://',
            creator=self.get_conn
        )

    def get_conn(self) -> pymysql.connections.Connection:
        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
        connector = Connector(ip_type)
        conn: pymysql.connections.Connection = connector.connect(
            self.instance,
            'pymysql',
            user=secret_manager.get_secret_tokens(DB_USER_KEY),
            password=secret_manager.get_secret_tokens(DB_PASS_KEY),
            db=secret_manager.get_secret_tokens(DB_NAME_KEY)
        )
        return conn

    def get_all_stock(self):
        conn = self.engine.connect()
        s = sqlalchemy.sql.select(Stock)
        result = conn.execute(s)
        for res in result:
            print(res)
