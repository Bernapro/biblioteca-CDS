from Persistencia.Postgres.PostgresOperable import PostgresOperable

class Usuario(PostgresOperable):

    def __init__(self, id_usuario, nombre, ap_paterno, ap_materno, fecha_nacimiento, tipo_usuario, identificador):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__ap_paterno = ap_paterno
        self.__ap_materno = ap_materno
        self.__fecha_nacimiento = fecha_nacimiento
        self.__tipo_usuario = tipo_usuario
        self.__identificador = identificador
    

    def get_table_name(self):
        return "usuario"
    
    def get_columns(self):
        self.columns = {"id_usuario": self.__id_usuario, "nombre": self.__nombre,
                        "ap_paterno": self.__ap_paterno, "ap_materno": self.__ap_materno,
                        "fecha_nacimiento": self.__fecha_nacimiento, "tipo_usuario": self.__tipo_usuario,
                        "identificador": self.__identificador}
        return self.columns
    
    def get_pkey(self):
        return self.id_usuario
    
    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        pass

    def getId_usuario(self):
        return self.__id_usuario
    
    def getNombre(self):
        return self.__nombre
    
    def getAp_paterno(self):
        return self.__ap_paterno
    
    def getAp_materno(self):
        return self.__ap_materno
    
    def getFecha_nacimiento(self):
        return self.__fecha_nacimiento
    
    def getTipo_usuario(self):
        return self.__tipo_usuario
    
    def getIdentificador(self):
        return self.__identificador
    
    def setId_usuario(self, id_usuario):
        self.__id_usuario = id_usuario
        
    def setNombre(self, nombre):
        self.__nombre = nombre
        
    def setAp_paterno(self, ap_paterno):
        self.__ap_paterno = ap_paterno  
    
    def setAp_materno(self, ap_materno):
        self.__ap_materno = ap_materno
        
    def setFecha_nacimiento(self, fecha_nacimiento):
        self.__fecha_nacimiento = fecha_nacimiento
        
    def setTipo_usuario(self, tipo_usuario):
        self.__tipo_usuario = tipo_usuario
        
    def setIdentificador(self, identificador):
        self.__identificador = identificador    