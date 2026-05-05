from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.CatalogoRepository import CatalogoRepository

class ControladorPantallaRegistroUsuario:
    def __init__(self, vista):
        self.__vista = vista  
        self.__repo_usuarios = RepositorioImpl(CRUDimp())
        self.__repo_catalogos = CatalogoRepository()

    def cargar_datos_iniciales(self):
        carreras = self.__repo_catalogos.obtener_carreras()
        semestres = self.__repo_catalogos.obtener_semestres()
        instituciones = self.__repo_catalogos.obtener_instituciones()

        return carreras, semestres, instituciones

    def actualizar_grupos(self, id_licenciatura, id_semestre):
        if not id_semestre or not id_licenciatura:
            return []
        return self.__repo_catalogos.obtener_grupos(id_licenciatura, id_semestre)

    def obtener_siguiente_vis(self):
        return self.__repo_usuarios.obtener_siguiente_vis()

    def guardar_usuario(self, datos_usuario, instancia_modelo):
        try:
            # Poblamos el modelo con el diccionario
            instancia_modelo.set_columns(datos_usuario)
            usr = instancia_modelo.getPadre()

            usr_persistente = self.__repo_usuarios.guardar(usr)

            if usr_persistente:
                instancia_modelo.setId_usuario(usr_persistente["id_usuario"])
                self.__repo_usuarios.guardar(instancia_modelo)

                return True, usr_persistente["identificador"]
            
            return False, None
            
        except Exception as ex:
            print("ERROR EN CONTROLADOR:", ex)
            if "usuario_identificador_key" in str(ex):
                raise ValueError("El usuario ya está registrado.")
            else:
                raise Exception("Error interno al guardar el usuario.")