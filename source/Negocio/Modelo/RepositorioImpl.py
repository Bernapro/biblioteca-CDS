from Negocio.Modelo.Interfaces.Repositorio import Repositorio
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db
import subprocess
from datetime import datetime
import os

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
##no se Usa paginado debido a filtros avanzados
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
        with db.get_connection() as conn:
            query = """
                SELECT last_value + 1 AS numero
                FROM seq_visitante
            """
            result = conn.execute(query).fetchone()
            return f"VIS-{result['numero']}"
        
    #
    def obtener_avanzado(
        self,
        nombre_tabla: str,
        filtros=None,
        or_filtros=None,
        limit=None,
        offset=None,
        order_by=None,
        columnas=None
    ):
        with db.get_connection() as conn:
            return self.__crud.read_advanced(
                conn=conn,
                nombre_tabla=nombre_tabla,
                filtros=filtros,
                or_filtros=or_filtros,
                limit=limit,
                offset=offset,
                order_by=order_by,
                columnas=columnas
            )

    def contar_avanzado(
        self,
        nombre_tabla,
        filtros=None,
        or_filtros=None
    ):
        with db.get_connection() as conn:
            return self.__crud.count_advanced(
                conn,
                nombre_tabla,
                filtros,
                or_filtros
            )

# =============================
    # DASHBOARD
    # =============================
    def obtener_estadisticas_dashboard(self):
        """Obtiene todos los conteos necesarios para el dashboard"""
        with db.get_connection() as conn:
            cur = conn.cursor() # 🔹 Cursor normal (devuelve tuplas, no diccionarios)
            
            # 1. Sesiones Hoy (Usuarios que entraron hoy)
            cur.execute("SELECT COUNT(*) FROM Registro WHERE DATE(fecha_entrada) = CURRENT_DATE")
            sesiones_hoy = cur.fetchone()[0] # 🔹 Accedemos al primer elemento
            
            # 2. Usuarios totales registrados
            cur.execute("SELECT COUNT(*) FROM Usuario")
            usuarios_totales = cur.fetchone()[0]
            
            # 3. Visitas totales históricas
            cur.execute("SELECT COUNT(*) FROM Registro")
            visitas_totales = cur.fetchone()[0]
            
            # 4. Incidencias Abiertas
            cur.execute("SELECT COUNT(*) FROM Incidencia WHERE estado = 'PENDIENTE'")
            incidencias_abiertas = cur.fetchone()[0]
            
            # 5. Visitas de la semana actual (Lunes a Domingo)
            query_semana = """
                SELECT EXTRACT(ISODOW FROM fecha_entrada) as dia, COUNT(*) as total
                FROM Registro
                WHERE fecha_entrada >= date_trunc('week', CURRENT_DATE)
                GROUP BY dia
            """
            cur.execute(query_semana)
            # row[0] es el día, row[1] es el total
            visitas_semana = {int(row[0]): row[1] for row in cur.fetchall()}
            
            return {
                "sesiones_hoy": sesiones_hoy,
                "usuarios_totales": usuarios_totales,
                "visitas_totales": visitas_totales,
                "incidencias_abiertas": incidencias_abiertas,
                "visitas_semana": visitas_semana
            }
        
    def backup_bd(self):
        try:
            import os
            from datetime import datetime
            import subprocess
            from Persistencia.Postgres.Pool.DBPool import db

            ruta = "backups"
            os.makedirs(ruta, exist_ok=True)

            hoy = datetime.now().strftime('%Y%m%d')
            archivo = f"{ruta}/backup_{hoy}.sql"

            if os.path.exists(archivo):
                return

            # 🔥 EXTRAER DATOS DEL POOL (SIN HARDCODE)
            conninfo = db._pool.conninfo  # ← aquí está todo

            # Convertir conninfo a variables
            partes = dict(item.split("=") for item in conninfo.split())

            env = os.environ.copy()
            env["PGPASSWORD"] = partes.get("password", "")

            subprocess.run([
                "pg_dump",
                "-U", partes.get("user"),
                "-h", partes.get("host", "localhost"),
                "-p", partes.get("port", "5432"),
                "-d", partes.get("dbname"),
                "-f", archivo
            ], check=True, env=env)

            print(f"✅ Backup creado: {archivo}")

        except Exception as e:
            print("❌ Error backup (no crítico):", e)

