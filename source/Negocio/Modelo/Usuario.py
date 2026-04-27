from Persistencia.Postgres.PostgresOperable import PostgresOperable

class Usuario(PostgresOperable):

    def __init__(self, id_usuario, nombre, ap_paterno, ap_materno, fecha_nacimiento, tipo_usuario, identificador):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno
        self.fecha_nacimiento = fecha_nacimiento
        self.tipo_usuario = tipo_usuario
        self.identificador = identificador
    
    def __init__(self):
        pass

    def get_table_name(self):
        return "usuario"
    
    def get_columns(self):
        self.columns = {"id_usuario": self.id_usuario, "nombre": self.nombre,
                        "ap_paterno": self.ap_paterno, "ap_materno": self.ap_materno,
                        "fecha_nacimiento": self.fecha_nacimiento, "tipo_usuario": self.tipo_usuario,
                        "identificador": self.identificador}
        return self.columns
    
    def get_pkey(self):
        return self.id_usuario
    
    def set_pkey(self, args):
        pass

    def set_columns(self, args):
        pass


    