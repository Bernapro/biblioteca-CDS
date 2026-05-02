from Persistencia.CRUD.CRUD import CRUD
from psycopg import sql, Connection
from psycopg.rows import dict_row

class CRUDimp(CRUD):

    def __init__(self):
        pass


#Autor: @bernapro

    #Si van a ocupar estas funciones tengan en cuenta que las hice pensando en que el bloque "with db.get_conn() as conn"
    #se ejecuta desde los controladores (o donde quiera que se manden a llamar las funciones) por ende se espera que se
    #pase como argumento una conexión activa del pool y no una instancia, esto con la finalidad de manejar las transacciones
    #por fuera, en caso de que se necesiten una o más funciones dentro del mismo proceso, recondar que al abrir el bloque
    #"with" con una conexión este ejecuta un BEGIN TRANSACTION, ROLLEBACK si se lanza una excepción en el proceso y COMMIT al finalizar
    #ese es el comportamiento por defecto

    #No es necesario especificar el tipo de dato de los parámetros ni tampoco el retorno de la función, pero de preferencia háganlo
    #así es más fácil entender que hace cada cosa

    #Insertar cualquier objeto que implemente la interfaz PostgresOperable
    def create(self, nombre_tabla: str, columnas: list, valores: list, conn: Connection) -> dict:
        query = sql.SQL(self.INSERT).format(
        tabla=sql.Identifier(nombre_tabla),
        columnas=sql.SQL(', ').join(map(sql.Identifier, columnas)),
        valores=sql.SQL(', ').join(sql.Placeholder() * len(columnas))
    )
        return conn.execute(query, valores).fetchone()

    #Obtener todos (para tablas sin muchos registros ó que sea necesario leer todo)
    def read_all(self,conn: Connection, nombre_tabla: str) -> list[dict]:
        query = sql.SQL(self.SELECT_COMODIN).format(
            tabla=sql.Identifier(nombre_tabla)
        )
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query)
            return cur.fetchall()
        
    #Obtener de manera paginada (para tablas que pueden llegar a tener muchos registros o si sólo se ocupan pocos)
    #el offset es el desplazamiento "LIMIT 10 OFFSET 20" trae 10 registros después de saltar los primeros 20
    #la idea es pedir la pagina y restarle 1 (pq las páginas inician en 0, en la primer página el offset es 0) 
    #para luego multiplicarlo por el número del LIMITde esa manera obtenemos el offset para usarlo cómo página 
    #p. ej. "pag = 3 tamaño_limit = 50 offset = (3-1) * tamaño_limit" entonces se saltará 100 registros y mostrará 
    #del 100 al 150 (la tercer página de 50)
 
    def get_paginated(self, conn: Connection, nombre_tabla: str, limit: int = 100, offset: int = 0) -> list[dict]:
        query = sql.SQL(self.SELECT_COMODIN_PAGINADO).format(
            tabla=sql.Identifier(nombre_tabla)
        )
        
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (limit, offset))
            return cur.fetchall()
        
    # -----------------------------------------------------------------------------------------------------------------



    def read_one(self, nombre_tabla, filtros, conn):
        condiciones = sql.SQL(" AND ").join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in filtros.keys()
        )

        query = sql.SQL("SELECT * FROM {} WHERE {} LIMIT 1").format(
            sql.Identifier(nombre_tabla),
            condiciones
        )

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

        return self.conn.execute(query, params).fetchall()

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

        return self.conn.execute(query, params).fetchone()

    def delete(self, nombre_tabla, filtros):
        where_clause = sql.SQL(" AND ").join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in filtros.keys()
        )

        query = sql.SQL("DELETE FROM {} WHERE {}").format(
            sql.Identifier(nombre_tabla),
            where_clause
        )

        self.conn.execute(query, tuple(filtros.values()))
