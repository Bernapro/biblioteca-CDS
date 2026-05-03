class ControladorPrestamos:
    def __init__(self, pantalla):
        self.__pantalla = pantalla

    def obtener_prestamos(self, busqueda="", estado="Todos"):
        # Aquí irá la consulta a la base de datos en el futuro
        # Por ahora, retornamos los datos simulados que estaban en la vista
        todos_los_datos = [
            {"matricula": "100025787", "nombre": "Carlos Daniel", "libro": "El principito", "estado": "A tiempo", "fecha_prestamo": "24/Mar/2026", "fecha_limite": "02/Abr/2026"},
            {"matricula": "100025788", "nombre": "Cruz Castillo", "libro": "1984", "estado": "Atrasado", "fecha_prestamo": "20/Mar/2026", "fecha_limite": "27/Mar/2026"},
            {"matricula": "ABCDEFGA", "nombre": "Jose Angel", "libro": "Clean Code", "estado": "A tiempo", "fecha_prestamo": "26/Mar/2026", "fecha_limite": "04/Abr/2026"},
            {"matricula": "ABCDEFGA", "nombre": "Figueroa Sales", "libro": "Python Básico", "estado": "Atrasado", "fecha_prestamo": "18/Mar/2026", "fecha_limite": "25/Mar/2026"},
        ]
        
        resultados = []
        for d in todos_los_datos:
            # Lógica de filtrado de negocio
            match_texto = busqueda.lower() in d["matricula"].lower() or busqueda.lower() in d["nombre"].lower() or busqueda.lower() in d["libro"].lower()
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