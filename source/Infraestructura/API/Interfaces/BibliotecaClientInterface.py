from abc import ABC, abstractmethod
from Infraestructura.API.Interfaces.Client import Client
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject

class BibliotecaClientInterface(Client):

    URL_BASE = "http://localhost:8080/biblioteca"


    def get(self) -> list[ResponseObject]:
        pass
    
    def get(self, nPage: int, len: int) -> list[ResponseObject]:
        pass

    def get(self, clave) -> ResponseObject:
        pass

    def post(self, args) -> ResponseObject:
        pass