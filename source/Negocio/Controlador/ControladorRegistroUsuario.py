from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db
from Persistencia.Postgres.PostgresOperable import PostgresOperable
from Negocio.Modelo.Usuario import Usuario


class ControladorPantallaRegistroUsuario():

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp(db))


    def guardar_usuario(self, e):
        id = e.control.data
        if id == "btn_guardar":
            instancia = self.__pantalla.usuarios[self.__pantalla.tipo_usuario.value]
            self.llenar_usuario(instancia)
            usr = instancia.getPadre()
            print(usr.get_columns())
            usrPersistente = self.__repo.guardar(usr)
            print(usrPersistente)
            if usrPersistente:
                instancia.setId_usuario(usrPersistente["id_usuario"])
                objPersistente = self.__repo.guardar(instancia)
                print(objPersistente)



    def data_usuario(self):
        return dict({"nombre": self.__pantalla.nombre.value, "ap_paterno": self.__pantalla.ap_paterno.value,
                      "ap_materno": self.__pantalla.ap_materno.value, "fecha_nacimiento": self.__pantalla.fecha_nacimiento.value, 
                      "tipo_usuario": self.__pantalla.tipo_usuario.value.upper(), "identificador": self.__pantalla.matricula.value, "semestre": self.__pantalla.semestre.value,
                      "grupo": self.__pantalla.grupo.value, "institucion": self.__pantalla.institucion.value, "licenciatura": self.__pantalla.licenciatura.value})
    
    def llenar_usuario(self, instancia:PostgresOperable):
            instancia = self.__pantalla.usuarios[self.__pantalla.tipo_usuario.value]
            instancia.set_columns(self.data_usuario())