from abc import ABC, abstractmethod
from Infraestructura.API.Interfaces.Client import Client
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
from Infraestructura.API.Interfaces.PageResponse import PageResponse
from Negocio.Modelo.Prestamo import Prestamo


class BibliotecaClientInterface(Client):

    URL_BASE = "http://localhost:8080/biblioteca"


    def get(self) -> list[ResponseObject]:
        pass
    
    def getPage(self, nPage: int, len: int) -> PageResponse[ResponseObject]:
        pass

    def get(self, clave) -> ResponseObject:
        pass

    def post(self, args) -> ResponseObject:
        pass

    def getEstado(self, parametro) -> ResponseObject:
        pass

    def patch(self, args) -> ResponseObject:
        pass