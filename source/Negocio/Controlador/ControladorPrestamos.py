from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos, BibliotecaClientInterface
from datetime import datetime



class ControladorPrestamos:
    def __init__(self, pantalla, endPrestamos: BibliotecaClientInterface):
        self.__pantalla = pantalla
        self.__endPrestamos = endPrestamos


    def obtener_prestamos(self, busqueda="", estado="Todos"):
        # Aquí irá la consulta a la base de datos en el futuro
        # Por ahora, retornamos los datos simulados que estaban en la vista
        print(self.__pantalla.texto_pagina.value)
        prestamos = self.__endPrestamos.getPage(nPage=int(self.__pantalla.texto_pagina.value)-1,len=10)
        datos = [{}]

        datos = [
        {
        "matricula": body["usuario"].getNombre() if body["usuario"] else "N/A", 
        "nombre": "Nombre Pendiente",
        "cantidad": str(body["cantidad"]),
        "estado": "Devuelto" if body["fechaDevolucion"] else ("Atrasado" if datetime.strptime(body["fechaLimite"], "%Y-%m-%d").date() <= datetime.now().date() else ("Por vencer" if (datetime.strptime(body["fechaLimite"], "%Y-%m-%d").date() - datetime.now().date()).days <= 3 else "A tiempo")), 
        "fecha_prestamo": body["fechaInicio"],
        "fecha_limite": body["fechaLimite"] 
        }
        for prestamo in prestamos.content 
        for body in [prestamo.getBody()]  
        ]
         
        resultados = []
        for d in datos:
            # Lógica de filtrado de negocio
            match_texto = busqueda.lower() in d["matricula"].lower() or busqueda.lower() in d["nombre"].lower() or busqueda.lower() in str(d["cantidad"]).lower()
            match_estado = (estado == "Todos") or (d["estado"] == estado)
            
            if match_texto and match_estado:
                resultados.append(d)
                
        return resultados

    def obtener_estadisticas(self):
        # Más adelante esto será un COUNT() a la base de datos
        return {
            "total": "4",
            "a_tiempo": "2",
            "atrasados": "2",
            "por_vencer": "0"
        }