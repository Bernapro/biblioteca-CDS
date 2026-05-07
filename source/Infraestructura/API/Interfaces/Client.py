from abc import ABC, abstractmethod
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
from Infraestructura.API.Interfaces.PageResponse import PageResponse
class Client(ABC):

    STATE_CODES = {200: "Operación exitosa", 404: "El recurso no existe", 500:"Error interno del servidor"}

    @abstractmethod
    def get(self) -> list[ResponseObject]:
        pass

    @abstractmethod
    def getPage(self, nPage: int, len: int) -> PageResponse[ResponseObject]:
        pass

    @abstractmethod
    def get(self, clave) -> ResponseObject:
        pass

    @abstractmethod
    def post(self, args) -> ResponseObject:
        pass

    @abstractmethod
    def getEstado(self, parametro) -> ResponseObject:
        pass

    @abstractmethod
    def patch(self, args) -> ResponseObject:
        pass