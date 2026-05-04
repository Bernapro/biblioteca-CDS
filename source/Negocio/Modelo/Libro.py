from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
from datetime import date
class Libro(ResponseObject):

    def __init__(self, isbn: str = "", titulo: str = "", autores: list[str] = None,
                  editorial: str = "", edicion: str = "", fechaPublicacion: date = None,
                  dewey: str = "", clasificaionDecimalUniversal: str = "", clasificacionDelCongreso: str = "",
                  categorias: list[str] = None):
            self.__isbn = isbn
            self.__titulo = titulo
            self.__autores = autores
            self.__editorial = editorial
            self.__edicion = edicion
            self.__fechaPublicacion = fechaPublicacion
            self.__dewey = dewey
            self.__clasificaionDecimalUniversal = clasificaionDecimalUniversal
            self.__clasificacionDelCongreso = clasificacionDelCongreso
            self.__categorias = categorias

    def setBody(self, args: dict) -> None:
        self.__isbn = args.get("isbn")
        self.__titulo = args.get("titulo")
        self.__autores = args.get("autores")
        self.__editorial = args.get("editorial")
        self.__edicion = args.get("edicion")
        self.__fechaPublicacion = args.get("fechaPublicacion") 
        self.__dewey = args.get("dewey")
        self.__clasificaionDecimalUniversal = args.get("clasificaionDecimalUniversal")
        self.__clasificacionDelCongreso = args.get("clasificacionDelCongreso")
        self.__categorias = args.get("categorias")

    def getBody(self) -> dict:
        return {"isbn": self.__isbn,
                "titulo": self.__titulo,
                "autores": self.__autores,
                "editorial": self.__editorial,
                "edicion": self.__edicion,
                "fechaPublicacion": self.__fechaPublicacion,
                "dewey": self.__dewey,
                "clasificaionDecimalUniversal": self.__clasificaionDecimalUniversal,
                "clasificacionDelCongreso": self.__clasificacionDelCongreso,
                "categorias": self.__categorias}
    
    def getISBN(self):
        return self.__isbn
    
    def getTitulo(self):
        return self.__titulo
    
    def getAutores(self):
        return self.__autores
    
    def getEditorial(self):
        return self.__editorial
    
    def getEdicion(self):
        return self.__edicion
    
    def getFechaPublicacion(self):
        return self.__fechaPublicacion
    
    def getDewey(self):
        return self.__dewey
    
    def getClasificaionDecimalUniversal(self):
        return self.__clasificaionDecimalUniversal
    
    def getClasificacionDelCongreso(self):
        return self.__clasificacionDelCongreso
    
    def getCategorias(self):
        return self.__categorias
    
    def setISBN(self, isbn):
        self.__isbn = isbn

    def setTitulo(self, titulo):
        self.__titulo = titulo

    def setAutores(self, autores):
        self.__autores = autores

    def setEditorial(self, editorial):
        self.__editorial = editorial

    def setEdicion(self, edicion):
        self.__edicion = edicion

    def setFechaPublicacion(self, fechaPublicacion):
        self.__fechaPublicacion = fechaPublicacion

    def setDewey(self, dewey):
        self.__dewey = dewey
    
    def setClasificaionDecimalUniversal(self, clasificaionDecimalUniversal):
        self.__clasificaionDecimalUniversal = clasificaionDecimalUniversal
    
    def setClasificacionDelCongreso(self, clasificacionDelCongreso):
        self.__clasificacionDelCongreso = clasificacionDelCongreso
    
    def setCategorias(self, categorias):
        self.__categorias = categorias