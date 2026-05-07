from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Negocio.Modelo.Incidencia import Incidencia
from datetime import datetime

class ControladorRegistroIncidencia:

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp())

    # BUSCAR USUARIO 
    def buscar_usuario(self, identificador):
        if not identificador or not str(identificador).strip():
            return None
        
        # Retorna el diccionario puro del usuario o None si no existe
        return self.__repo.buscar_usuario_por_identificador(identificador)


    # GUARDAR INCIDENCIA
    def guardar_incidencia(self, datos_incidencia):
        try:
            incidencia = Incidencia()
            
            incidencia.set_data(datos_incidencia)

            resultado = self.__repo.guardar(incidencia)

            if resultado:
                return True, resultado
            return False, "No se pudo guardar la incidencia en la base de datos."

        except Exception as ex:
            print("💥 ERROR EN CONTROLADOR:", ex)
            return False, "Error interno al procesar la solicitud."