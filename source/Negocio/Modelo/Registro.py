from Persistencia.Postgres.PostgresOperable import PostgresOperable

class Registro(PostgresOperable):

    def __init__(self, id_registro=None, id_usuario=None):
        self._id_registro = id_registro
        self._id_usuario = id_usuario

    def get_table_name(self):
        return "registro"

    def get_columns(self):
        return {
            "id_usuario": self._id_usuario
        }

    def get_pkey(self):
        return self._id_registro

    def set_pkey(self, args):
        self._id_registro = args.get("id_registro")

    def set_columns(self, args):
        self._id_usuario = args.get("id_usuario")

    def getIdRegistro(self):
        return self._id_registro

    def getIdUsuario(self):
        return self._id_usuario

    def setIdRegistro(self, id_registro):
        self._id_registro = id_registro

    def setIdUsuario(self, id_usuario):
        self._id_usuario = id_usuario