from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class CatalogoRepository:

    def __init__(self):
        self._pool = db

    # CARRERAS
    def obtener_carreras(self):
        query = "SELECT id_carrera, nombre_carrera FROM carrera ORDER BY nombre_carrera"
        with self._pool.get_connection() as conn:
            return conn.execute(query).fetchall()

    # SEMESTRES
    def obtener_semestres(self):
        query = "SELECT id_semestre, semestre FROM semestre ORDER BY id_semestre"
        with self._pool.get_connection() as conn:
            return conn.execute(query).fetchall()

    # INSTITUCIONES
    def obtener_instituciones(self):
        query = "SELECT id_institucion, nombre_institucion FROM institucion ORDER BY nombre_institucion"
        with self._pool.get_connection() as conn:
            return conn.execute(query).fetchall()

    # GRUPOS FILTRADOS
    def obtener_grupos(self, id_carrera, id_semestre):
        query = """
            SELECT id_grupo, grupo
            FROM grupo
            WHERE id_carrera = %s AND id_semestre = %s
            ORDER BY grupo
        """
        with self._pool.get_connection() as conn:
            return conn.execute(query, (id_carrera, id_semestre)).fetchall()