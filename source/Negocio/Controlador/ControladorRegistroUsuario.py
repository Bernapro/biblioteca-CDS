from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.CatalogoRepository import CatalogoRepository
from Negocio.Modelo.Alumno import Alumno
from Negocio.Modelo.Personal import Personal
from Negocio.Modelo.Visitante import Visitante

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

    # 🔹 2. Ya no recibe "instancia_modelo", solo recibe el diccionario de la UI
    def guardar_usuario(self, datos_usuario):
        try:
            tipo = datos_usuario.get("tipo_usuario", "").upper()

            # 🔹 3. El Controlador toma la decisión de qué modelo crear
            if tipo == "ALUMNO":
                instancia_modelo = Alumno()
            elif tipo == "PERSONAL":
                instancia_modelo = Personal()
            elif tipo == "VISITANTE":
                instancia_modelo = Visitante()
            else:
                raise ValueError("Tipo de usuario no válido")

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