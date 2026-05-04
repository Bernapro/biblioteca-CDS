from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject

class BibliotecaPrestamos(BibliotecaClientInterface):

    ENDPOINT = "/prestamos"

    def __init__(self):
        pass

    def get(self) -> list[ResponseObject]:
        pass
    
    def get(self,nPage: int, len: int) -> list[ResponseObject]:
        pass

    def get(self,clave) -> ResponseObject:
        pass