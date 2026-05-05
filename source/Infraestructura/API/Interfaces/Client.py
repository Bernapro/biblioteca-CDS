from abc import ABC, abstractmethod
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
class Client(ABC):

    STATE_CODES = {200: "Operación exitosa", 404: "El recurso no existe", 500:"Error interno del servidor"}

    @abstractmethod
    def get(self) -> list[ResponseObject]:
        pass

    @abstractmethod
    def get(self, nPage: int, len: int) -> list[ResponseObject]:
        pass

    @abstractmethod
    def get(self, clave) -> ResponseObject:
        pass

    @abstractmethod
    def post(self, args) -> ResponseObject:
        pass