from psycopg.rows import dict_row
from Persistencia.Postgres.Pool.DBPool import db
from Negocio.Modelo.Interfaces.ReporteRepository import ReporteRepository


class ReporteRepositoryImpl(ReporteRepository):

    def obtener_asistencia_completa(self, fecha_inicio, fecha_fin, tipo_usuario=None):

        query = """
        SELECT
            identificador,
            nombre_completo,
            tipo_usuario,
            fecha_entrada,
            fecha_salida,

            CASE
                WHEN fecha_salida IS NULL
                THEN 'ACTIVO'
                ELSE 'FINALIZADO'
            END AS estado,

            COALESCE(
                fecha_salida - fecha_entrada,
                NOW() - fecha_entrada
            ) AS tiempo_estadia,

            grupo,
            semestre,
            nombre_carrera,
            nombre_facultad,
            nombre_institucion

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')
        """

        params = [fecha_inicio, fecha_fin]

        if tipo_usuario:
            query += " AND tipo_usuario = %s"
            params.append(tipo_usuario)

        query += " ORDER BY fecha_entrada DESC"

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, tuple(params))

                return cur.fetchall()
            
    def obtener_usuarios_mas_activos(
        self,
        fecha_inicio,
        fecha_fin,
        tipo_usuario=None
    ):

        query = """
        SELECT

            identificador,
            nombre_completo,
            tipo_usuario,

            COUNT(*) AS visitas,

            COALESCE(
                SUM(
                    EXTRACT(EPOCH FROM (
                        COALESCE(fecha_salida, NOW()) - fecha_entrada
                    ))
                ),
                0
            ) AS segundos_totales,

            COALESCE(
                AVG(
                    EXTRACT(EPOCH FROM (
                        COALESCE(fecha_salida, NOW()) - fecha_entrada
                    ))
                ),
                0
            ) AS promedio_segundos,

            MAX(fecha_entrada) AS ultima_visita

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')

        """

        params = [fecha_inicio, fecha_fin]

        if tipo_usuario:
            query += " AND tipo_usuario = %s"
            params.append(tipo_usuario)

        query += """

        GROUP BY
            identificador,
            nombre_completo,
            tipo_usuario

        ORDER BY visitas DESC

        LIMIT 20
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, tuple(params))

                resultados = cur.fetchall()

                # convertir segundos → horas legibles
                for r in resultados:

                    r["horas_totales"] = round(
                        r["segundos_totales"] / 3600,
                        2
                    )

                    r["promedio_horas"] = round(
                        r["promedio_segundos"] / 3600,
                        2
                    )

                return resultados

    def obtener_horas_pico_avanzado(
        self,
        fecha_inicio,
        fecha_fin
    ):

        query = """
        SELECT

            EXTRACT(HOUR FROM fecha_entrada) AS hora,

            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN tipo_usuario = 'ALUMNO'
                    THEN 1
                    ELSE 0
                END
            ) AS alumnos,

            SUM(
                CASE
                    WHEN tipo_usuario = 'PERSONAL'
                    THEN 1
                    ELSE 0
                END
            ) AS personal,

            SUM(
                CASE
                    WHEN tipo_usuario = 'VISITANTE'
                    THEN 1
                    ELSE 0
                END
            ) AS visitantes

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')


        GROUP BY hora

        ORDER BY hora
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, (fecha_inicio, fecha_fin))

                return cur.fetchall()

    def obtener_tendencia_diaria(
        self,
        fecha_inicio,
        fecha_fin,
        tipo_usuario=None
    ):

        query = """
        SELECT

            DATE(fecha_entrada) AS fecha,

            COUNT(*) AS total_usuarios,

            SUM(
                CASE
                    WHEN tipo_usuario = 'ALUMNO'
                    THEN 1
                    ELSE 0
                END
            ) AS alumnos,

            SUM(
                CASE
                    WHEN tipo_usuario = 'PERSONAL'
                    THEN 1
                    ELSE 0
                END
            ) AS personal,

            SUM(
                CASE
                    WHEN tipo_usuario = 'VISITANTE'
                    THEN 1
                    ELSE 0
                END
            ) AS visitantes

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')

        """

        params = [fecha_inicio, fecha_fin]

        if tipo_usuario:
            query += " AND tipo_usuario = %s"
            params.append(tipo_usuario)

        query += """

        GROUP BY fecha

        ORDER BY fecha
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, tuple(params))

                return cur.fetchall()

    def obtener_reporte_carreras(
        self,
        fecha_inicio,
        fecha_fin
    ):

        query = """
        SELECT

            COALESCE(
                nombre_carrera,
                'SIN CARRERA'
            ) AS carrera,

            COUNT(*) AS total_visitas,

            COUNT(DISTINCT id_usuario) AS usuarios_unicos,

            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            COALESCE(fecha_salida, NOW()) - fecha_entrada
                        )
                    ) / 3600
                ),
                2
            ) AS promedio_horas

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')


        AND tipo_usuario = 'ALUMNO'

        GROUP BY nombre_carrera

        ORDER BY total_visitas DESC
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, (fecha_inicio, fecha_fin))

                return cur.fetchall()

    def obtener_reporte_facultades(
        self,
        fecha_inicio,
        fecha_fin
    ):

        query = """
        SELECT

            COALESCE(
                nombre_facultad,
                'SIN FACULTAD'
            ) AS facultad,

            COUNT(*) AS total_visitas,

            COUNT(DISTINCT id_usuario) AS usuarios_unicos,

            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            COALESCE(fecha_salida, NOW()) - fecha_entrada
                        )
                    ) / 3600
                ),
                2
            ) AS promedio_horas

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')


        GROUP BY nombre_facultad

        ORDER BY total_visitas DESC
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, (fecha_inicio, fecha_fin))

                return cur.fetchall()

    def obtener_reporte_semestres(
        self,
        fecha_inicio,
        fecha_fin
    ):

        query = """
        SELECT

            COALESCE(
                CAST(semestre AS TEXT),
                'SIN SEMESTRE'
            ) AS semestre,

            COUNT(*) AS total_visitas,

            COUNT(DISTINCT id_usuario) AS usuarios_unicos,

            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            COALESCE(fecha_salida, NOW()) - fecha_entrada
                        )
                    ) / 3600
                ),
                2
            ) AS promedio_horas

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')

        AND tipo_usuario = 'ALUMNO'

        GROUP BY semestre

        ORDER BY
        CASE
            WHEN semestre ~ '^[0-9]+$'
            THEN CAST(semestre AS INTEGER)
            ELSE 999
        END
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, (fecha_inicio, fecha_fin))

                return cur.fetchall()

    def obtener_visitantes_externos(
        self,
        fecha_inicio,
        fecha_fin
    ):

        query = """
        SELECT

            COALESCE(
                nombre_institucion,
                'SIN INSTITUCIÓN'
            ) AS institucion,

            COUNT(*) AS total_visitas,

            COUNT(DISTINCT id_usuario) AS usuarios_unicos,

            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            COALESCE(fecha_salida, NOW()) - fecha_entrada
                        )
                    ) / 3600
                ),
                2
            ) AS promedio_horas

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')

        AND tipo_usuario = 'VISITANTE'

        GROUP BY nombre_institucion

        ORDER BY total_visitas DESC
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, (fecha_inicio, fecha_fin))

                return cur.fetchall()

    def obtener_reporte_saturacion(
        self,
        fecha_inicio,
        fecha_fin
    ):

        query = """
        SELECT

            EXTRACT(HOUR FROM fecha_entrada) AS hora,

            COUNT(*) AS total_usuarios,

            COUNT(*) FILTER (
                WHERE tipo_usuario = 'ALUMNO'
            ) AS alumnos,

            COUNT(*) FILTER (
                WHERE tipo_usuario = 'PERSONAL'
            ) AS personal,

            COUNT(*) FILTER (
                WHERE tipo_usuario = 'VISITANTE'
            ) AS visitantes

        FROM vista_historial

        WHERE fecha_entrada >= %s
        AND fecha_entrada < (%s::date + INTERVAL '1 day')


        GROUP BY hora

        ORDER BY total_usuarios DESC
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query, (fecha_inicio, fecha_fin))

                return cur.fetchall()

    def obtener_reporte_crecimiento(self):

        query = """
        SELECT

            TO_CHAR(
                DATE_TRUNC('month', fecha_entrada),
                'YYYY-MM'
            ) AS mes,

            COUNT(*) AS total_visitas,

            COUNT(DISTINCT id_usuario) AS usuarios_unicos,

            COUNT(*) FILTER (
                WHERE tipo_usuario = 'ALUMNO'
            ) AS alumnos,

            COUNT(*) FILTER (
                WHERE tipo_usuario = 'PERSONAL'
            ) AS personal,

            COUNT(*) FILTER (
                WHERE tipo_usuario = 'VISITANTE'
            ) AS visitantes

        FROM vista_historial

        GROUP BY DATE_TRUNC('month', fecha_entrada)

        ORDER BY DATE_TRUNC('month', fecha_entrada)
        """

        with db.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute(query)

                return cur.fetchall()





