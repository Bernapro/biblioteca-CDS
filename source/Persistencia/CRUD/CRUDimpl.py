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

    def execute_procedure(self, procedure_name: str, conn: Connection):
        """Ejecuta un procedimiento SQL sin parámetros"""
        query = sql.SQL("CALL {}()").format(sql.Identifier(procedure_name))
        conn.execute(query)
   # =========================
    # MOTOR DE FILTROS AVANZADO
    # =========================
    def read_advanced(
        self,
        conn: Connection,
        nombre_tabla: str,
        filtros: dict = None,
        or_filtros: list[dict] = None,
        limit: int = None,
        offset: int = None,
        order_by: list[tuple[str, str]] = None,
        columnas: list[str] = None
    ) -> list[dict]:

        # =========================
        # SELECT dinámico
        # =========================
        if columnas:
            query = sql.SQL("SELECT {} FROM {}").format(
                sql.SQL(", ").join(map(sql.Identifier, columnas)),
                sql.Identifier(nombre_tabla)
            )
        else:
            query = sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(nombre_tabla)
            )

        valores = []
        condiciones = []

        # =========================
        # FUNCIÓN INTERNA PARA OPERADORES
        # =========================
        def procesar_filtro(key, value):
            if "__" not in key:
                return (
                    sql.SQL("{} = {}").format(sql.Identifier(key), sql.Placeholder()),
                    [value]
                )

            campo, op = key.split("__", 1)

            if op == "like":
                return (
                    sql.SQL("{} ILIKE {}").format(sql.Identifier(campo), sql.Placeholder()),
                    [f"%{value}%"]
                )

            elif op == "in":
                if not value:
                    return (sql.SQL("FALSE"), [])
                placeholders = sql.SQL(", ").join(sql.Placeholder() * len(value))
                return (
                    sql.SQL("{} IN ({})").format(sql.Identifier(campo), placeholders),
                    list(value)
                )

            elif op == "between":
                return (
                    sql.SQL("{} BETWEEN {} AND {}").format(
                        sql.Identifier(campo),
                        sql.Placeholder(),
                        sql.Placeholder()
                    ),
                    list(value)
                )

            elif op == "gte":
                return (
                    sql.SQL("{} >= {}").format(sql.Identifier(campo), sql.Placeholder()),
                    [value]
                )

            elif op == "lte":
                return (
                    sql.SQL("{} <= {}").format(sql.Identifier(campo), sql.Placeholder()),
                    [value]
                )

            elif op == "isnull":
                return (sql.SQL("{} IS NULL").format(sql.Identifier(campo)), [])

            elif op == "notnull":
                return (sql.SQL("{} IS NOT NULL").format(sql.Identifier(campo)), [])

            else:
                raise ValueError(f"Operador no soportado: {op}")

        # =========================
        # AND filtros
        # =========================
        if filtros:
            for key, value in filtros.items():
                condicion, vals = procesar_filtro(key, value)
                condiciones.append(condicion)
                valores.extend(vals)

        # =========================
        # OR filtros (YA AVANZADO)
        # =========================
        if or_filtros:
            grupos = []
            for grupo in or_filtros:
                sub_condiciones = []
                for key, value in grupo.items():
                    condicion, vals = procesar_filtro(key, value)
                    sub_condiciones.append(condicion)
                    valores.extend(vals)

                grupos.append(
                    sql.SQL("(") + sql.SQL(" AND ").join(sub_condiciones) + sql.SQL(")")
                )

            condiciones.append(
                sql.SQL("(") + sql.SQL(" OR ").join(grupos) + sql.SQL(")")
            )

        # =========================
        # WHERE
        # =========================
        if condiciones:
            query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(condiciones)

        # =========================
        # ORDER BY
        # =========================
        if order_by:
            orden = []
            for campo, direccion in order_by:
                direccion = direccion.upper()
                if direccion not in ("ASC", "DESC"):
                    raise ValueError("Dirección inválida en ORDER BY")

                orden.append(
                    sql.SQL("{} {}").format(
                        sql.Identifier(campo),
                        sql.SQL(direccion)
                    )
                )

            query += sql.SQL(" ORDER BY ") + sql.SQL(", ").join(orden)

        # =========================
        # PAGINACIÓN
        # =========================
        if limit is not None:
            query += sql.SQL(" LIMIT {}").format(sql.Literal(limit))

        if offset is not None:
            query += sql.SQL(" OFFSET {}").format(sql.Literal(offset))

        # =========================
        # EJECUCIÓN
        # =========================
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, valores)
            return cur.fetchall()


    def count_advanced(
        self,
        conn,
        nombre_tabla,
        filtros=None,
        or_filtros=None
    ):
        query = f"SELECT COUNT(*) as total FROM {nombre_tabla}"
        condiciones = []
        valores = []

        # 🔹 filtros AND
        if filtros:
            for key, value in filtros.items():
                if "__" in key:
                    campo, op = key.split("__")

                    if op == "like":
                        condiciones.append(f"{campo} ILIKE %s")
                        valores.append(f"%{value}%")

                    elif op == "gte":
                        condiciones.append(f"{campo} >= %s")
                        valores.append(value)

                    elif op == "lte":
                        condiciones.append(f"{campo} <= %s")
                        valores.append(value)

                    elif op == "isnull":
                        condiciones.append(f"{campo} IS NULL")

                    elif op == "notnull":
                        condiciones.append(f"{campo} IS NOT NULL")
                else:
                    condiciones.append(f"{key} = %s")
                    valores.append(value)

        # 🔹 filtros OR
        if or_filtros:
            or_condiciones = []
            for f in or_filtros:
                for key, value in f.items():
                    campo, op = key.split("__")
                    if op == "like":
                        or_condiciones.append(f"{campo} ILIKE %s")
                        valores.append(f"%{value}%")

            if or_condiciones:
                condiciones.append("(" + " OR ".join(or_condiciones) + ")")

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        return conn.execute(query, tuple(valores)).fetchone()["total"]