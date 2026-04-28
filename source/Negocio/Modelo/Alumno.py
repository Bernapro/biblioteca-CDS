from Negocio.Modelo.Usuario import Usuario

class Alumno(Usuario):

    def __init__(self, id_usuario= None, nombre= "", ap_paterno= "", ap_materno= "", fecha_nacimiento= None, tipo_usuario= "", identificador= "", grupo= None, semestre= None, licenciatura= None):
        super().__init__(id_usuario, nombre, ap_paterno, ap_materno, fecha_nacimiento, tipo_usuario, identificador)
        self.__grupo = grupo
        self.__semestre = semestre
        self.__licenciatura = licenciatura



    def get_table_name(self):
        return "alumno"

    def get_columns(self):
        columns = super().get_columns()
        columns_alumno= {"id_usuario": self._id_usuario,"matricula": columns["identificador"],"id_grupo": self.__grupo}
        return columns_alumno
    
    def get_pkey(self):
        return self._id_usuario
    
    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        super().set_columns(args)
        self.__grupo = args["grupo"]
        self.__semestre = args["semestre"]
        self.__licenciatura = args["licenciatura"]


    def getGrupo(self):
        return self.__grupo
    
    def setGrupo(self, grupo):
        self.__grupo = grupo

    def getSemestre(self):
        return self.__semestre  
    
    def setSemestre(self, semestre):
        self.__semestre = semestre

    def getLicenciatura(self):
        return self.__licenciatura
        
    def setLicenciatura(self, licenciatura):
        self.__licenciatura = licenciatura

    def getPadre(self):
        return Usuario(self._id_usuario, self._nombre, self._ap_paterno, self._ap_materno, self._fecha_nacimiento, self._tipo_usuario, self._identificador)