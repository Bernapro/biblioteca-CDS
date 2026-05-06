from Infraestructura.API.Interfaces.ResponseObject import ResponseObject


class ReporteEstadoPrestamo(ResponseObject):

    def __init__(self):
        pass

    def setBody(self, args: dict) -> None:
        self.__total = args.get("totales")
        self.__vigentes = args.get("vigentes")
        self.__vencidos = args.get("vencidos")
        self.__proximosAVencer = args.get("proximosAVencer")

    def getBody(self) -> dict:
        return {"totales": self.__total,
                "vigentes": self.__vigentes,
                "vencidos": self.__vencidos,
                "proximosAVencer": self.__proximosAVencer}

    def getTotales(self):
        return self.__total

    def getVigentes(self):
        return self.__vigentes

    def getVencidos(self):
        return self.__vencidos

    def getProximosAVencer(self):
        return self.__proximosAVencer

    def setTotales(self, total):
        self.__total = total

    def setVigentes(self, vigentes):
        self.__vigentes = vigentes

    def setVencidos(self, vencidos):
        self.__vencidos = vencidos

    def setProximosAVencer(self, proximosAVencer):
        self.__proximosAVencer = proximosAVencer

