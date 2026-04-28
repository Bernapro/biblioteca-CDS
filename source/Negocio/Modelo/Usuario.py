from Persistencia.Postgres.PostgresOperable import PostgresOperable

class Usuario(PostgresOperable):

    def __init__(self, id_usuario= None, nombre= "", ap_paterno= "", ap_materno= "", fecha_nacimiento= None, tipo_usuario= "", identificador= ""):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._ap_paterno = ap_paterno
        self._ap_materno = ap_materno
        self._fecha_nacimiento = fecha_nacimiento
        self._tipo_usuario = tipo_usuario
        self._identificador = identificador
    

    def get_table_name(self):
        return "usuario"
    
    def get_columns(self):
        self.columns = {"nombre": self._nombre,
                        "ap_paterno": self._ap_paterno, "ap_materno": self._ap_materno,
                        "fecha_nacimiento": self._fecha_nacimiento, "tipo_usuario": self._tipo_usuario,
                        "identificador": self._identificador}
        return self.columns
    
    def get_pkey(self):
        return self.id_usuario
    
    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        self._nombre = args["nombre"]
        self._ap_paterno = args["ap_paterno"]
        self._ap_materno = args["ap_materno"]
        self._fecha_nacimiento = args["fecha_nacimiento"]
        self._tipo_usuario = args["tipo_usuario"]
        self._identificador = args["identificador"]


    def getId_usuario(self):
        return self._id_usuario
    
    def getNombre(self):
        return self._nombre
    
    def getAp_paterno(self):
        return self._ap_paterno
    
    def getAp_materno(self):
        return self._ap_materno
    
    def getFecha_nacimiento(self):
        return self._fecha_nacimiento
    
    def getTipo_usuario(self):
        return self._tipo_usuario
    
    def getIdentificador(self):
        return self._identificador
    
    def setId_usuario(self, id_usuario):
        self._id_usuario = id_usuario
        
    def setNombre(self, nombre):
        self._nombre = nombre
        
    def setAp_paterno(self, ap_paterno):
        self._ap_paterno = ap_paterno  
    
    def setAp_materno(self, ap_materno):
        self._ap_materno = ap_materno
        
    def setFecha_nacimiento(self, fecha_nacimiento):
        self._fecha_nacimiento = fecha_nacimiento
        
    def setTipo_usuario(self, tipo_usuario):
        self._tipo_usuario = tipo_usuario
        
    def setIdentificador(self, identificador):
        self._identificador = identificador    

    def getPadre(self):
        pass