from Persistencia.CRUD.CRUD import CRUD
from psycopg import sql

class CRUDimp(CRUD):

    def __init__(self, pool):
        self.pool = pool


    def create(self, nombre_tabla, columnas, valores):
        query = sql.SQL(self.INSERT).format(
        tabla=sql.Identifier(nombre_tabla),
        columnas=sql.SQL(', ').join(map(sql.Identifier, columnas)),
        valores=sql.SQL(', ').join(sql.Placeholder() * len(columnas))
    )
        with self.pool.get_connection() as conn:
            return conn.execute(query, valores).fetchone()
        
