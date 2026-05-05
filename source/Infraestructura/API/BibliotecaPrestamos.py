from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
import requests
from Negocio.Modelo.Prestamo import Prestamo
from Negocio.Modelo.Usuario import Usuario





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

    def post(self, args) -> ResponseObject:
        if not args:
            return None
        url = f"{self.URL_BASE+self.ENDPOINT}"
        prestamo = None
        r = requests.post(url,json=args)
        try:
            print(self.STATE_CODES[r.status_code])
        except KeyError:
            print("Código de respuesta desconocido")
        if r.status_code == 201:
            args = r.json()
            prestamo = Prestamo(id= args["id"], fechaLimite= args["fechaLimite"], cantidad= args["cantidad"], usuario= Usuario())
            usr = prestamo.getUsuario()
            usr.setIdentificador(args["usuario"])
            print(prestamo.getBody())


