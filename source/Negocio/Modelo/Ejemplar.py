from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
from Negocio.Modelo.Libro import Libro
import uuid

class Ejemplar(ResponseObject):

    def __init__(self, id: uuid = None, noAdquisicion:str = "", libro: Libro = None,
                    estado: str = "", condicion: str = "", ):
        self.__id = id
        self.__noAdquisicion = noAdquisicion
        self.__libro = libro
        self.__estado = estado
        self.__condicion = condicion

    def setBody(self, args: dict) -> None:
        self.__id = args.get("id")
        self.__noAdquisicion = args.get("noAdquisicion")
        self.__libro = args.get("libro")
        self.__estado = args.get("estado")
        self.__condicion = args.get("condicion")

    def getBody(self) -> dict:
        return {"id": self.__id,
                "noAdquisicion": self.__noAdquisicion,
                "libro": self.__libro,
                "estado": self.__estado,
                "condicion": self.__condicion}
    
    def getid(self):
        return self.__id
    
    def getNoAdquisicion(self):
        return self.__noAdquisicion
    
    def getLibro(self):
        return self.__libro
    
    def getEstado(self):
        return self.__estado
    
    def getCondicion(self):
        return self.__condicion
    
    def setId(self, UUID):
        self.__id = UUID
    
    def setNoAdquisicion(self, noAdquisicion):
        self.__noAdquisicion = noAdquisicion
    
    def setLibro(self, libro):
        self.__libro = libro
    
    def setEstado(self, estado):
        self.__estado = estado
    
    def setCondicion(self, condicion):
        self.__condicion = condicion

    