from Negocio.Modelo.Usuario import Usuario

class Personal(Usuario):

    def __init__(self, id_usuario=None, nombre="", ap_paterno="", ap_materno="", 
                 fecha_nacimiento=None, tipo_usuario="", identificador="", n_plaza=""):
        
        super().__init__(id_usuario, nombre, ap_paterno, ap_materno, 
                         fecha_nacimiento, tipo_usuario, identificador)
        
        self.__n_plaza = n_plaza


    def get_table_name(self):
        return "personal"

    def get_columns(self):
        columns = super().get_columns()
        columns_personal = {
            "id_usuario": self._id_usuario,
            "n_plaza": columns["identificador"]
        }
        return columns_personal

    def get_pkey(self):
        return self._id_usuario

    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        super().set_columns(args)
        self.__n_plaza = args["n_plaza"]

    def getPlaza(self):
        return self.__n_plaza

    def setPlaza(self, n_plaza):
        self.__n_plaza = n_plaza

    def getPadre(self):
        return Usuario(
            self._id_usuario,
            self._nombre,
            self._ap_paterno,
            self._ap_materno,
            self._fecha_nacimiento,
            self._tipo_usuario,
            self._identificador
        )