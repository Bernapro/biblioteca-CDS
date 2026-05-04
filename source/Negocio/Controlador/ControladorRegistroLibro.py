import re
from Infraestructura.API.libros_api import crear_libro, autocompletar_libro

class ControladorRegistroLibro:

    def crear_libro(self, data):

        # VALIDACIONES
        if not data["isbn"] or not data["titulo"]:
            return {"ok": False, "mensaje": "ISBN y Título son obligatorios"}

        try:
            n_ejemplares = int(data["nEjemplares"])
        except:
            return {"ok": False, "mensaje": "Cantidad inválida"}

        data["nEjemplares"] = n_ejemplares

        # LLAMADA API
        response = crear_libro(data)

        if response.status_code == 201:
            return {"ok": True, "mensaje": "Libro registrado correctamente"}

        return {
            "ok": False,
            "mensaje": f"Error API: {response.text}"
        }
    
    def buscar_por_isbn(self, isbn):

        isbn_limpio = isbn.replace("-", "").strip()

        if not re.fullmatch(r"^(?:\d{9}[\dXx]|\d{13})$", isbn_limpio):
            return {"ok": False, "mensaje": "ISBN inválido"}

        response = autocompletar_libro(isbn_limpio)

        if response is None:
            return {"ok": False, "mensaje": "Error de conexión con la API"}

        if response.status_code != 200:
            return {"ok": False, "mensaje": "No se encontró el libro"}

        libro = response.json()

        return {
            "ok": True,
            "data": {
                "titulo": libro.get("titulo", ""),
                "editorial": libro.get("editorial", ""),
                "fecha": str(libro.get("fechaPublicacion", "")),
                "autores": list(libro.get("autores", [])),
                "categorias": list(libro.get("categorias", [])),
                "edicion": libro.get("edicion", "") or "",
                "dewey": libro.get("dewey", "") or "",
                "cdu": libro.get("cdu", "") or "",
                "lcc": libro.get("lcc", "") or ""
            }
        }