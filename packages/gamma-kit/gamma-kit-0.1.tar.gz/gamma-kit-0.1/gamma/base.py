import psycopg2
from .errors import DatabaseError


class Database:
    def __init__(self, database='app_db', **kwargs):
        self.conn = psycopg2.connect(
            dbname=database,
            user=kwargs.get('user'),
            password=kwargs.get('password'),
            host=kwargs.get('host'),
            port=kwargs.get('port')
        )

        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to execute query.") from e

    def fetch(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch data.") from e

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            raise DatabaseError("Failed to close the database connection.") from e
