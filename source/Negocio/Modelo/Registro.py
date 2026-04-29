from Persistencia.Postgres.PostgresOperable import PostgresOperable


class Registro(PostgresOperable):

    def __init__(
        self,
        id_registro=None,
        id_usuario=None,
        fecha=None,
        hora_entrada=None,
        hora_salida=None
    ):
        self._id_registro = id_registro
        self._id_usuario = id_usuario
        self._fecha = fecha
        self._hora_entrada = hora_entrada
        self._hora_salida = hora_salida


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
        self._fecha = args.get("fecha")
        self._hora_entrada = args.get("hora_entrada")
        self._hora_salida = args.get("hora_salida")

    def getIdRegistro(self):
        return self._id_registro

    def getIdUsuario(self):
        return self._id_usuario

    def getFecha(self):
        return self._fecha

    def getHoraEntrada(self):
        return self._hora_entrada

    def getHoraSalida(self):
        return self._hora_salida

    def setIdRegistro(self, id_registro):
        self._id_registro = id_registro

    def setIdUsuario(self, id_usuario):
        self._id_usuario = id_usuario

    def setFecha(self, fecha):
        self._fecha = fecha

    def setHoraEntrada(self, hora):
        self._hora_entrada = hora

    def setHoraSalida(self, hora):
        self._hora_salida = hora