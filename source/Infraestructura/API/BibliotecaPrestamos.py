from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
import requests
from Negocio.Modelo.Prestamo import Prestamo
from Negocio.Modelo.Usuario import Usuario
from Infraestructura.API.Interfaces.PageResponse import PageResponse
from Infraestructura.API.Interfaces.PageMetadata import PageMetadata
from Negocio.Modelo.ReporteEstadoPrestamo import ReporteEstadoPrestamo





class BibliotecaPrestamos(BibliotecaClientInterface):

    ENDPOINT = "/prestamos"

    def __init__(self):
        pass

    def get(self) -> list[ResponseObject]:
        pass

    def getPage(self, nPage: int, len: int) -> PageResponse[Prestamo]:
        print("En función de pagina")
        page = nPage if nPage else 0
        len_p = len if len else 10
        url = f"{self.URL_BASE}{self.ENDPOINT}?"
        args = {
            "nPage": page,
            "len": len_p
        }
        
        r = requests.get(url, params=args)
        
        try:
            print(self.STATE_CODES[r.status_code])
        except KeyError:
            print("Código de respuesta desconocido")
            return PageResponse[Prestamo]()
            
        if r.status_code == 200:
            body = r.json()
            
            lista_prestamos = [
                Prestamo(
                    id=item["id"],
                    fechaLimite=item["fechaLimite"],
                    fechaInicio=item["fechaInicio"],
                    fechaDevolucion=item["fechaDevolucion"],
                    cantidad=item["cantidad"],
                    usuario=Usuario(identificador=item["usuario"])
                )
                for item in body.get("contenido", [])
            ]
            
            metadatos = PageMetadata(
                total_pages=body.get("totalPaginas", 0),
                total_elements=body.get("totalElementos", 0),
                size=body.get("tamanoPagina", len_p),
                number=body.get("numeroPagina", page),
                last=body.get("ultima", True)
            )
            
            return PageResponse[Prestamo](content=lista_prestamos, metadata=metadatos)
            
        return PageResponse[Prestamo]()
            


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

    def getEstado(self, parametro = 3) -> ResponseObject:
        url = f"{self.URL_BASE+self.ENDPOINT}/estado/{parametro}"
        r = requests.get(url)
        try:
            print(self.STATE_CODES[r.status_code])
        except KeyError:
            print("Código de respuesta desconocido")
        if r.status_code == 200:
            args = r.json()
            reporte = ReporteEstadoPrestamo()
            reporte.setBody(args)
            return reporte





