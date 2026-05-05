from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
import uuid
from Negocio.Modelo.Ejemplar import Ejemplar
from Negocio.Modelo.Usuario import Usuario
from datetime import datetime
class Prestamo(ResponseObject):

    def __init__(self, id: uuid= None, fechaInicio: datetime= None, fechaLimite: datetime= None
                 , fechaDevolucion: datetime= None, usuario: Usuario= None, ejemplares:list[Ejemplar]= None
                 , cantidad: int=0):
        self.__id = id
        self.__fechaInicio = fechaInicio
        self.__fechaLimite = fechaLimite
        self.__fechaDevolucion = fechaDevolucion
        self.__usuario = usuario
        self.__ejemplares = ejemplares
        self.__cantidad = cantidad

    def getBody(self):
        return {"id": self.__id,
                "fechaInicio": self.__fechaInicio,
                "fechaLimite": self.__fechaLimite,
                "fechaDevolucion": self.__fechaDevolucion,
                "usuario": self.__usuario,
                "ejemplares": self.__ejemplares,
                "cantidad": self.__cantidad}

    def setBody(self, args):
        self.__id = args.get("id")
        self.__fechaInicio = args.get("fechaInicio")
        self.__fechaLimite = args.get("fechaLimite")
        self.__fechaDevolucion = args.get("fechaDevolucion")   
        self.__usuario = args.get("usuario")
        self.__ejemplares = args.get("ejemplares")
        self.__cantidad = args.get("cantidad")

    def getId(self):
        return self.__id  
    def getFechaInicio(self):
        return self.__fechaInicio
    def getFechaLimite(self):
        return self.__fechaLimite
    def getFechaDevolucion(self):
        return self.__fechaDevolucion
    def getUsuario(self):
        return self.__usuario
    def getEjemplares(self):
        return self.__ejemplares
    def getCantidad(self):
        return self.__cantidad
    def setId(self, id):
        self.__id = id
    def setFechaInicio(self, fechaInicio):
        self.__fechaInicio = fechaInicio
    def setFechaLimite(self, fechaLimite):
        self.__fechaLimite = fechaLimite
    def setFechaDevolucion(self, fechaDevolucion):
        self.__fechaDevolucion = fechaDevolucion
    def setUsuario(self, usuario):
        self.__usuario = usuario
    def setEjemplares(self, ejemplares):
        self.__ejemplares = ejemplares
    def setCantidad(self, cantidad):
        self.__cantidad = cantidad