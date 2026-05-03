from Persistencia.Postgres.PostgresOperable import PostgresOperable


class Incidencia(PostgresOperable):

    def __init__(self):
        self._id_incidencia = None
        self._id_usuario = None
        self._tipo = None
        self._motivo = None
        self._descripcion = None
        self._lugar = None

    # =========================
    # TABLA
    # =========================
    def get_table_name(self):
        return "incidencia"

    # =========================
    # COLUMNAS
    # =========================
    def get_columns(self):
        return {
            "id_usuario": self._id_usuario,
            "tipo": self._tipo,
            "motivo": self._motivo,
            "descripcion": self._descripcion or "",
            "lugar": self._lugar or ""
        }

    # =========================
    # SET DATA (TU MÉTODO)
    # =========================
    def set_data(self, data):
        self._id_usuario = data["id_usuario"]
        self._tipo = data["tipo"]
        self._motivo = data["motivo"]
        self._descripcion = data["descripcion"]
        self._lugar = data["lugar"]

    # =========================
    # 🔥 OBLIGATORIOS (ESTE ERA TU ERROR)
    # =========================

    def get_pkey(self):
        return "id_incidencia"

    def set_pkey(self, value):
        self._id_incidencia = value

    def set_columns(self, data: dict):
        self._id_usuario = data.get("id_usuario")
        self._tipo = data.get("tipo")
        self._motivo = data.get("motivo")
        self._descripcion = data.get("descripcion")
        self._lugar = data.get("lugar")