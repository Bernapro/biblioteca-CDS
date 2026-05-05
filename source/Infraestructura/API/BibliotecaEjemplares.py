from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
import requests
from Negocio.Modelo.Libro import Libro
from Negocio.Modelo.Ejemplar import Ejemplar


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
        ejem = None
        url = f"{self.URL_BASE+self.ENDPOINT}/{clave}"
        r = requests.get(url)
        try:
            print(self.STATE_CODES[r.status_code])
        except KeyError:
            print("Código de respuesta desconocido")
        if r.status_code == 200:
            args = r.json()
            ejem = Ejemplar(id = args["id"], noAdquisicion= args["noAdquisicion"], libro= Libro(), disponible= args["disponible"])
            lib = ejem.getLibro()
            lib.setTitulo(args["titulo"])
            lib.setAutores(args["autores"])

        return ejem
    
    def post(self, args) -> ResponseObject:
        pass