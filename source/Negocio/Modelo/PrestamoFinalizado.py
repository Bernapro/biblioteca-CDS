from Negocio.Modelo.Prestamo import Prestamo

class PrestamoFinalizado(Prestamo):

    def __init__(self, id=None, fechaInicio=None, fechaLimite=None, fechaDevolucion=None, usuario=None, ejemplares=None, cantidad=0, comentario = ""):
        super().__init__(id, fechaInicio, fechaLimite, fechaDevolucion, usuario, ejemplares, cantidad)
        self.__comentario = comentario

    def getComentario(self):
        return self.__comentario

    def setComentario(self, comentario):
        self.__comentario = comentario

    def getBody(self):
        body = super().getBody()
        body["comentario"] = self.__comentario
        return body

    def setBody(self, args):
        super().setBody(args)
        self.__comentario = args.get("comentario")

