class ControladorIncidencia:
    def __init__(self, pantalla):
        self.__pantalla = pantalla

    def obtener_incidencias(self):
        # Aquí en el futuro iría la consulta a la base de datos a través de tu Repositorio
        # Por ahora, retornamos los datos simulados para que la vista los dibuje
        return [
            {
                "nombre": "Carlos Daniel", "matricula": "100025787", 
                "carrera": "Ingeniería en Sistemas", "semestre": "4° Semestre", 
                "razon": "Ruido excesivo", "lugar": "Cubículo 1", 
                "fecha": "24/Marzo/2026 - 10:30 AM", "tipo": "PARCIAL", "estado": "Pendiente"
            },
            {
                "nombre": "Cruz Castillo", "matricula": "100025788", 
                "carrera": "Lic. en Derecho", "semestre": "6° Semestre", 
                "razon": "Uso indebido del equipo", "lugar": "Cubículo 2", 
                "fecha": "25/Marzo/2026 - 11:00 AM", "tipo": "DEFINITIVA", "estado": "Resuelto"
            },
            {
                "nombre": "Jose Angel", "matricula": "ABCDEFGA", 
                "carrera": "Medicina", "semestre": "2° Semestre", 
                "razon": "Comportamiento inapropiado", "lugar": "Cubículo 3", 
                "fecha": "26/Marzo/2026 - 09:15 AM", "tipo": "PARCIAL", "estado": "Pendiente"
            },
            {
                "nombre": "Figueroa Sales", "matricula": "ABCDEFGA", 
                "carrera": "Contaduría", "semestre": "8° Semestre", 
                "razon": "Páginas arrancadas", "lugar": "Área de lectura", 
                "fecha": "27/Marzo/2026 - 16:00 PM", "tipo": "DEFINITIVA", "estado": "Resuelto"
            },
        ]

    def guardar_dialogo(self, e):
        # Lógica de negocio: extraemos los datos desde la vista
        nombre = self.__pantalla.modal_nombre.value
        comentario = self.__pantalla.modal_comentario.value
        
        print(f"Controlador: Guardando cambios para {nombre} | Comentario: {comentario}")
        
        # Después de guardar (ej. en BD), cerramos el modal a través de la vista
        self.__pantalla.cerrar_dialogo(e)