from Negocio.Modelo.Usuario import Usuario

class Visitante(Usuario):

    def __init__(self, id_usuario=None, nombre="", ap_paterno="", ap_materno="", 
                 fecha_nacimiento=None, tipo_usuario="", identificador="", id_institucion=None):
        
        super().__init__(id_usuario, nombre, ap_paterno, ap_materno, 
                         fecha_nacimiento, tipo_usuario, identificador)
        
        self.__id_institucion = id_institucion


    def get_table_name(self):
        return "visitante"

    def get_columns(self):
        columns = super().get_columns()
        columns_visitante = {
            "id_usuario": self._id_usuario,
            "id_institucion": self.__id_institucion
        }
        return columns_visitante

    def get_pkey(self):
        return self._id_usuario

    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        super().set_columns(args)
        self.__id_institucion = args["institucion"]   # ✔

    def getInstitucion(self):
        return self.__id_institucion

    def setInstitucion(self, id_institucion):
        self.__id_institucion = id_institucion

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