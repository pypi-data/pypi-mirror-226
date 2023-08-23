from bewe.services.crawler import secret_manager
from typing import Any, Sequence
import mysql.connector


DB_HOST_KEY = 'DB_HOST'
DB_USER_KEY = 'DB_USER'
DB_PASS_KEY = 'DB_PASS'


class DBManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=secret_manager.get_secret_tokens(DB_HOST_KEY),
            user=secret_manager.get_secret_tokens(DB_USER_KEY),
            password=secret_manager.get_secret_tokens(DB_PASS_KEY)
        )

    def execute_query(self, sql: str) -> Sequence[Any]:
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = []

        for row in result:
            result.append(row)
        return result
