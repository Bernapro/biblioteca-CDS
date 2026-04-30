from Negocio.Modelo.Interfaces.Repositorio import Repositorio
from Persistencia.CRUD.CRUDimpl import CRUDimp

class RepositorioImpl(Repositorio):

    def __init__(self, crud: CRUDimp):
        self.__crud = crud


#registro
    def obtener_todos(self, nombre_tabla: str):
        return self.__crud.read_all(nombre_tabla)

    def obtener_por_id(self, nombre_tabla: str, id):
        return self.__crud.read_one(
            nombre_tabla,
            {f"id_{nombre_tabla}": id}
        )

    def guardar(self, objeto):
        if self.__crud:
            valores = tuple(objeto.get_columns().values())
            return self.__crud.create(objeto.get_table_name(), objeto.get_columns().keys(), valores)
        return None
        
    def eliminar(self, nombre_tabla: str, id):
        return self.__crud.delete(
            nombre_tabla,
            {f"id_{nombre_tabla}": id}
        )
    
    def obtener_siguiente_vis(self):
        query = "SELECT last_value + 1 AS siguiente FROM seq_visitante"

        with self._RepositorioImpl__crud.pool.get_connection() as conn:
            result = conn.execute(query).fetchone()
            return f"VIS-{result['siguiente']}"

    #asistencia
    def buscar_usuario_por_identificador(self, identificador):
        return self.__crud.read_one(
            "usuario",
            {"identificador": identificador}
        )

    def obtener_registro_abierto(self, id_usuario):
        query = """
            SELECT *
            FROM registro
            WHERE id_usuario = %s
            AND fecha_salida IS NULL
            ORDER BY fecha_entrada DESC
            LIMIT 1
        """

        with self._RepositorioImpl__crud.pool.get_connection() as conn:
            return conn.execute(query, (id_usuario,)).fetchone()

    def registrar_salida(self, id_registro):
        query = """
            UPDATE registro
            SET fecha_salida = CURRENT_TIMESTAMP
            WHERE id_registro = %s
            RETURNING *
        """

        with self._RepositorioImpl__crud.pool.get_connection() as conn:
            return conn.execute(query, (id_registro,)).fetchone()
        
    def cerrar_registros_abiertos(self):
        query = """
            UPDATE registro
            SET fecha_salida = DATE_TRUNC('day', fecha_entrada) + INTERVAL '23:59:59'
            WHERE fecha_salida IS NULL
            AND fecha_entrada < CURRENT_DATE
        """

        with self._RepositorioImpl__crud.pool.get_connection() as conn:
            conn.execute(query)
            
#historial
    def obtener_historial(self):
        query = """
            SELECT 
                u.identificador,
                u.nombre,
                u.ap_paterno,
                u.ap_materno,
                r.fecha_entrada,
                r.fecha_salida
            FROM registro r
            INNER JOIN usuario u 
                ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_entrada DESC
        """

        with self._RepositorioImpl__crud.pool.get_connection() as conn:
            return conn.execute(query).fetchall()
        
