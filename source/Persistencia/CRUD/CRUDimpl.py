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

    def read_one(self, nombre_tabla, filtros):
        condiciones = sql.SQL(" AND ").join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in filtros.keys()
        )

        query = sql.SQL("SELECT * FROM {} WHERE {} LIMIT 1").format(
            sql.Identifier(nombre_tabla),
            condiciones
        )

        with self.pool.get_connection() as conn:
            return conn.execute(query, tuple(filtros.values())).fetchone()

    def read_all(self, nombre_tabla, filtros=None):
        if filtros:
            condiciones = sql.SQL(" AND ").join(
                sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
                for k in filtros.keys()
            )

            query = sql.SQL("SELECT * FROM {} WHERE {}").format(
                sql.Identifier(nombre_tabla),
                condiciones
            )

            params = tuple(filtros.values())
        else:
            query = sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(nombre_tabla)
            )
            params = ()

        with self.pool.get_connection() as conn:
            return conn.execute(query, params).fetchall()

    def update(self, nombre_tabla, columnas, filtros):
        set_clause = sql.SQL(', ').join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in columnas.keys()
        )

        where_clause = sql.SQL(" AND ").join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in filtros.keys()
        )

        query = sql.SQL("UPDATE {} SET {} WHERE {} RETURNING *").format(
            sql.Identifier(nombre_tabla),
            set_clause,
            where_clause
        )

        params = tuple(columnas.values()) + tuple(filtros.values())

        with self.pool.get_connection() as conn:
            return conn.execute(query, params).fetchone()

    def delete(self, nombre_tabla, filtros):
        where_clause = sql.SQL(" AND ").join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in filtros.keys()
        )

        query = sql.SQL("DELETE FROM {} WHERE {}").format(
            sql.Identifier(nombre_tabla),
            where_clause
        )

        with self.pool.get_connection() as conn:
            conn.execute(query, tuple(filtros.values()))