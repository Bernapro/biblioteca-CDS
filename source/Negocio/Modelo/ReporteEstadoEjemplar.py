from Infraestructura.API.Interfaces.ResponseObject import ResponseObject


class ReporteEstadoEjemplar(ResponseObject):

    def __init__(self):
        pass

    def setBody(self, args: dict) -> None:
        self.__total = args.get("totales")
        self.__prestados = args.get("prestados")
        self.__disponibles = args.get("disponibles")
    def getBody(self) -> dict:
        return {"totales": self.__total,
                "prestados": self.__prestados,
                "disponibles": self.__disponibles
        }
    def getTotales(self):
        return self.__total

    def getPrestados(self):
        return self.__prestados

    def getDisponibles(self):
        return self.__disponibles

    def setTotales(self, total):
        self.__total = total

    def setPrestados(self, prestados):
        self.__prestados = prestados

    def setDisponibles(self, disponibles):
        self.__disponibles = disponibles

