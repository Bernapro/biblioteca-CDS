from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
import requests

class BibliotecaEjemplares(BibliotecaClientInterface):
    
    ENDPOINT = "/ejemplares"

    def __init__(self):
        pass

    def get(self) -> list[ResponseObject]:
        pass
    
    def get(self, nPage: int, len: int) -> list[ResponseObject]:
        pass

    def get(self, clave = "") -> ResponseObject:
        if not clave:
            return None
        url = f"{self.URL_BASE+self.ENDPOINT}/{clave}"
        r = requests.get(url)
        try:
            print(self.STATE_CODES[r.status_code])
        except KeyError:
            print("Código de respuesta desconocido")
        if r.status_code == 200:
            print(r.json())
        return None