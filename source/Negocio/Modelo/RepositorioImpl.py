from Negocio.Modelo.Interfaces.Repositorio import Repositorio
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class RepositorioImpl(Repositorio):

    def __init__(self, crud: CRUDimp):
        self.__crud = crud

    # =============================
    # INTERFAZ (SE RESPETA TAL CUAL)
    # =============================

    def obtener_todos(self, nombre_tabla: str):
        with db.get_connection() as conn:
            return self.__crud.read_all(conn, nombre_tabla)

    def obtener_por_id(self, nombre_tabla: str, id):
        with db.get_connection() as conn:
            return self.__crud.read_one(
                nombre_tabla,
                {f"id_{nombre_tabla}": id},
                conn
            )

    def guardar(self, objeto):
        with db.get_connection() as conn:
            valores = tuple(objeto.get_columns().values())
            return self.__crud.create(
                objeto.get_table_name(),
                objeto.get_columns().keys(),
                valores,
                conn
            )

    def eliminar(self, nombre_tabla: str, id):
        with db.get_connection() as conn:
            return self.__crud.delete(
                nombre_tabla,
                {f"id_{nombre_tabla}": id},
                conn
            )

    def obtener_paginado(self, nombre_tabla: str, limit: int = 10, offset: int = 0):
        with db.get_connection() as conn:
            return self.__crud.get_paginated(conn, nombre_tabla, limit, offset)

    def buscar_usuario_por_identificador(self, identificador):
        with db.get_connection() as conn:
            return self.__crud.read_one(
                "usuario",
                {"identificador": identificador},
                conn
            )

    def ejecutar_procedimiento(self, nombre_procedimiento: str):
        """Ejecuta un procedimiento SQL (ej: cerrar_registros_pendientes)"""
        with db.get_connection() as conn:
            self.__crud.execute_procedure(nombre_procedimiento, conn)

    # =============================
    # ASISTENCIA (OPERACIONES ESPECÍFICAS)
    # =============================

    def obtener_registro_abierto(self, id_usuario):
        """Obtiene registro sin salida para un usuario (para asistencia)"""
        with db.get_connection() as conn:
            query = """
                SELECT *
                FROM registro
                WHERE id_usuario = %s
                AND fecha_salida IS NULL
                LIMIT 1
            """
            return conn.execute(query, (id_usuario,)).fetchone()

    def registrar_salida(self, id_registro):
        """Registra hora de salida (para asistencia)"""
        with db.get_connection() as conn:
            query = """
                UPDATE registro
                SET fecha_salida = CURRENT_TIMESTAMP
                WHERE id_registro = %s
                RETURNING *
            """
            return conn.execute(query, (id_registro,)).fetchone()

    # =============================
    # REGISTRO DE USUARIOS
    # =============================

    def obtener_siguiente_vis(self):
        """Obtiene el siguiente número de secuencia para Visitante"""
        with db.get_connection() as conn:
            query = "SELECT nextval('seq_visitante') as numero"
            result = conn.execute(query).fetchone()
            return f"VIS-{result['numero']}"
        