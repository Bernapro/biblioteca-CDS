import atexit
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row


class DBPoolBiblioteca:
    def __init__(self, conninfo: str):
        self._pool = ConnectionPool(
            conninfo,
            min_size=2,
            max_size=4,
            max_idle=600,
            check=ConnectionPool.check_connection,
            kwargs={"row_factory": dict_row}
        )

        print("Pool de biblioteca creado correctamente")
        print(conninfo)

        atexit.register(self.close_pool)

    def get_connection(self):
        return self._pool.connection()

    def close_pool(self):
        if not self._pool.closed:
            self._pool.close()
            print("Pool de biblioteca cerrado correctamente.")


db_biblioteca = DBPoolBiblioteca(
    "dbname=biblioteca user=postgres password=292005"
)