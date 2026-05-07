from Negocio.Modelo.Interfaces.Repositorio import Repositorio
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db

class RepositorioImpl(Repositorio):

    def __init__(self, crud: CRUDimp):
        self.__crud = crud


    def obtener_por_bloque(self, pks: list = [], tabla: str = "", columna: str = ""):
        with db.get_connection() as conn:
            return self.__crud.get_by_pk_batch(conn = conn, nombre_tabla =tabla, nombre_columna_pk = columna, lista_pks = pks)

    # INTERFAZ 

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

    def ejecutar_procedimiento(self, nombre_procedimiento):
        with db.get_connection() as conn:
            self.__crud.execute_procedure(nombre_procedimiento, conn)
            conn.commit()

    # ASISTENCIA 

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

    # REGISTRO DE USUARIOS
    def obtener_siguiente_vis(self):

        with db.get_connection() as conn:

            query = """
                SELECT COALESCE(
                    MAX(
                        CAST(
                            REPLACE(identificador, 'VIS-', '') AS INTEGER
                        )
                    ),
                0) + 1 AS siguiente
                FROM usuario
                WHERE identificador LIKE 'VIS-%'
            """

            result = conn.execute(query).fetchone()

            return f"VIS-{result['siguiente']}"
            
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
#DASHBOARD PRIMER CUADRO
    def contar_sesiones_activas_hoy(self):
        with db.get_connection() as conn:
            query = """
                SELECT COUNT(*) AS total
                FROM registro
                WHERE DATE(fecha_entrada) = CURRENT_DATE
                AND fecha_salida IS NULL
            """
            result = conn.execute(query).fetchone()
            return result["total"] if isinstance(result, dict) else result[0]

    # DASHBOARD
    def obtener_estadisticas_dashboard(self):
        """Obtiene todos los conteos necesarios para el dashboard"""
        with db.get_connection() as conn:
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) AS total FROM registro WHERE DATE(fecha_entrada) = CURRENT_DATE")
            row = cur.fetchone()
            sesiones_hoy = row["total"] if isinstance(row, dict) else row[0]
            
            cur.execute("SELECT COUNT(*) AS total FROM usuario")
            row = cur.fetchone()
            usuarios_totales = row["total"] if isinstance(row, dict) else row[0]
            
            cur.execute("SELECT COUNT(*) AS total FROM registro")
            row = cur.fetchone()
            visitas_totales = row["total"] if isinstance(row, dict) else row[0]
            
            cur.execute("SELECT COUNT(*) AS total FROM incidencia WHERE estado = 'PENDIENTE'")
            row = cur.fetchone()
            incidencias_abiertas = row["total"] if isinstance(row, dict) else row[0]
            
            query_semana = """
                SELECT EXTRACT(ISODOW FROM fecha_entrada) as dia, COUNT(*) as total
                FROM registro
                WHERE fecha_entrada >= date_trunc('week', CURRENT_DATE)
                GROUP BY dia
            """
            cur.execute(query_semana)
            visitas_semana = {int(row["dia"]): row["total"] for row in cur.fetchall()}
            
            return {
                "sesiones_hoy": sesiones_hoy,
                "usuarios_totales": usuarios_totales,
                "visitas_totales": visitas_totales,
                "incidencias_abiertas": incidencias_abiertas,
                "visitas_semana": visitas_semana
            }
        
    def obtener_pg_dump(self):
        import os
        from shutil import which

        pg = which("pg_dump")
        if pg:
            return pg

        versiones = range(18, 9, -1)

        for v in versiones:
            ruta = fr"C:\Program Files\PostgreSQL\{v}\bin\pg_dump.exe"
            if os.path.exists(ruta):
                return ruta

        raise FileNotFoundError("No se encontró pg_dump en el sistema")


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

            conninfo = db._pool.conninfo
            partes = dict(item.split("=") for item in conninfo.split())

            env = os.environ.copy()
            env["PGPASSWORD"] = partes.get("password", "")

            # 🔥 AQUÍ ESTÁ LA CLAVE
            pg_dump = self.obtener_pg_dump()

            subprocess.run([
                pg_dump,
                "-U", partes.get("user"),
                "-h", partes.get("host", "localhost"),
                "-p", partes.get("port", "5432"),
                "-d", partes.get("dbname"),
                "-f", archivo
            ], check=True, env=env)

            print(f"✅ Backup creado: {archivo}")

        except Exception as e:
            print("❌ Error backup (no crítico):", e)
