from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db
from Persistencia.Postgres.PostgresOperable import PostgresOperable
from Negocio.Modelo.Usuario import Usuario


class ControladorPantallaRegistroUsuario():

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp())


    def guardar_usuario(self, e):
        id = e.control.data
        if id == "btn_guardar":
            instancia = self.__pantalla.usuarios[self.__pantalla.tipo_usuario.value]

            self.llenar_usuario(instancia)

            usr = instancia.getPadre()

            # Guardar usuario base
            usrPersistente = self.__repo.guardar(usr)

            if usrPersistente:
                instancia.setId_usuario(usrPersistente["id_usuario"])

                # Guardar subtipo (Alumno, Personal o Visitante)
                objPersistente = self.__repo.guardar(instancia)

                # Regresar identificador
                return {
                    "id_usuario": usrPersistente["id_usuario"],
                    "identificador": usrPersistente["identificador"]
                }
        return None

    def data_usuario(self):
        tipo = self.__pantalla.tipo_usuario.value.upper()

        identificador = self.__pantalla.matricula.value

        if tipo == "VISITANTE":
            identificador = None

        return dict({
            "nombre": self.__pantalla.nombre.value,
            "ap_paterno": self.__pantalla.ap_paterno.value,
            "ap_materno": self.__pantalla.ap_materno.value,
            "fecha_nacimiento": self.__pantalla.fecha_nacimiento.value,
            "tipo_usuario": tipo,
            "identificador": identificador,
            "semestre": self.__pantalla.semestre.value,
            "grupo": self.__pantalla.grupo.value,
            "institucion": self.__pantalla.institucion.value,
            "licenciatura": self.__pantalla.licenciatura.value
        })
    

    def obtener_siguiente_vis(self):
        return self.__repo.obtener_siguiente_vis()

    def llenar_usuario(self, instancia:PostgresOperable):
            instancia = self.__pantalla.usuarios[self.__pantalla.tipo_usuario.value]
            instancia.set_columns(self.data_usuario())