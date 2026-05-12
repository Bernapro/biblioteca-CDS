from Infraestructura.API.BibliotecaPrestamos import BibliotecaClientInterface
from datetime import datetime
from Negocio.Utilidades.FormatearFecha import FormatearFecha
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Negocio.Modelo.Usuario import Usuario



class ControladorPrestamos:

    def __init__(self, pantalla, endPrestamos: BibliotecaClientInterface, repo: RepositorioImpl):
        self.__pantalla = pantalla
        self.__endPrestamos = endPrestamos
        self.__repo = repo

    def obtenerLibros(self, id = ""):
        print(id)
        datos = [{}]
        if id:
            lista = self.__endPrestamos.getDetalle(id)
            print(lista)
            if lista:
                datos = [
                    {
                    "titulo": body["libro"].getTitulo() if body["libro"] else "N/A",
                    "autor": ", ".join(body["libro"].getAutores()) if body["libro"] else "N/A",
                    "adq": body["noAdquisicion"], 
                    }
                    for ejemplar in lista 
                    for body in [ejemplar.getBody()]  
                ]
        return datos


    def obtener_prestamos(self, busqueda="", estado="Todos"):
        # Aquí irá la consulta a la base de datos en el futuro
        # Por ahora, retornamos los datos simulados que estaban en la vista
        prestamos = self.__endPrestamos.getPage(nPage=int(self.__pantalla.pagina_actual)-1,len=10)
        datos = [{}]
        identificadores = [prestamo.getUsuario().getIdentificador() for prestamo in prestamos.content]
        diccionarios = self.__repo.obtener_por_bloque(pks=identificadores, tabla="usuario", columna="identificador")
        usuarios_dict = {
        datos["identificador"]: Usuario(**datos) 
        for datos in diccionarios
        }
        self.__pantalla.total_registros = prestamos.metadata.total_elements
        
        datos = [
        {
        "prestamo": body["id"],
        "identificador": body["usuario"].getIdentificador() if body["usuario"] else "N/A", 
        "nombre": usuarios_dict[body["usuario"].getIdentificador()].getNombre() if body["usuario"] else "N/A",
        "cantidad": str(body["cantidad"]),
        "estado": "Devuelto" if body["fechaDevolucion"] else ("Atrasado" if datetime.strptime(body["fechaLimite"], "%Y-%m-%d").date() < datetime.now().date() else ("Por vencer" if (datetime.strptime(body["fechaLimite"], "%Y-%m-%d").date() - datetime.now().date()).days <= 3 else "A tiempo")), 
        "fecha_prestamo": FormatearFecha.formatear_fecha_iso(body["fechaInicio"]),
        "fecha_limite": FormatearFecha.formatear_fecha_iso(body["fechaLimite"]) 
        }
        for prestamo in prestamos.content 
        for body in [prestamo.getBody()]  
        ]
         
        resultados = []
        for d in datos:
            # Lógica de filtrado de negocio
            match_texto = busqueda.lower() in d["identificador"].lower() or busqueda.lower() in d["nombre"].lower() or busqueda.lower() in str(d["cantidad"]).lower()
            match_estado = (estado == "Todos") or (d["estado"] == estado)
            
            if match_texto and match_estado:
                resultados.append(d)
        return resultados

    def obtener_estadisticas(self):
        #  adelante esto será un COUNT() a la base de datos
        return self.__endPrestamos.getEstado().getBody()
    
    def finalizarPrestamo(self, e, prestamo):
        msg = "El préstamo ya fue devuelto" if prestamo[1] == "Devuelto" else "No se puede realizar esta operacion"
        color = "orange" if prestamo[1] == "Devuelto" else "red"
        if prestamo[1] != "Devuelto":
            res = self.__endPrestamos.patch(prestamo[0])
            if res:
                dict = res.getBody()
                msg = dict["comentario"]
                print(dict["comentario"])
                color = "green"
        boton = e.control
        if boton:
            boton.visible = False
        self.__pantalla.cargar_datos()
        self.__pantalla.mostrar_mensaje(msg, color)