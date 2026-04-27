from Modelo.Usuario import Usuario

class Alumno(Usuario):

    def __init__(self, id_usuario, nombre, ap_paterno, ap_materno, fecha_nacimiento, tipo_usuario, identificador, grupo):
        super().__init__(id_usuario, nombre, ap_paterno, ap_materno, fecha_nacimiento, tipo_usuario, identificador)
        self.__grupo = grupo


    def get_table_name(self):
        return "alumno"

    def get_columns(self):
        columns = super().get_columns()
        columns_alumno= {"id": columns["id_usuario"],"matricula": columns["identificador"],"grupo": self.__grupo}
        return columns_alumno
    
    def get_pkey(self):
        return self.__id_usuario
    
    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        pass

    def getGrupo(self):
        return self.__grupo
    def setGrupo(self, grupo):
        self.__grupo = grupo