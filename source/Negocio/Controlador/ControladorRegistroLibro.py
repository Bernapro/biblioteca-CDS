import re
from Infraestructura.API.libros_api import crear_libro, autocompletar_libro


class ControladorRegistroLibro:

    def crear_libro(self, data):

        if (
            not data["isbn"]
            or not data["titulo"]
            or not data["editorial"]
            or not data["fechaPublicacion"]
            or not data["nEjemplares"]
        ):
            return {
                "ok": False,
                "mensaje": "Completa todos los campos obligatorios"
            }

        if not data["autores"]:
            return {
                "ok": False,
                "mensaje": "Debes ingresar al menos un autor"
            }

        try:
            n_ejemplares = int(data["nEjemplares"])

            if n_ejemplares <= 0:
                return {
                    "ok": False,
                    "mensaje": "La cantidad de ejemplares debe ser mayor a 0"
                }

        except ValueError:
            return {
                "ok": False,
                "mensaje": "Cantidad de ejemplares inválida"
            }

        data["nEjemplares"] = n_ejemplares

        response = crear_libro(data)

        if response is None:
            return {
                "ok": False,
                "mensaje": "No se pudo conectar con el servidor"
            }

        if response.status_code == 201:
            return {
                "ok": True,
                "mensaje": "Libro registrado correctamente"
            }

        if response.status_code == 400:
            return {
                "ok": False,
                "mensaje": "Datos inválidos para registrar el libro"
            }

        if response.status_code >= 500:
            return {
                "ok": False,
                "mensaje": "Error interno del servidor"
            }

        return {
            "ok": False,
            "mensaje": "No se pudo registrar el libro"
        }

    def buscar_por_isbn(self, isbn):

        isbn_limpio = isbn.replace("-", "").strip()

        if not re.fullmatch(r"^(?:\d{9}[\dXx]|\d{13})$", isbn_limpio):
            return {
                "ok": False,
                "mensaje": "Formato de ISBN inválido"
            }

        try:
            response = autocompletar_libro(isbn_limpio)

            if response is None:
                return {
                    "ok": False,
                    "mensaje": "No se pudo conectar con el servicio de búsqueda ISBN"
                }

            if response.status_code == 404:
                return {
                    "ok": False,
                    "mensaje": "ISBN no encontrado"
                }

            if response.status_code >= 500:
                return {
                    "ok": False,
                    "mensaje": "Error del servidor al consultar ISBN"
                }

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

        except Exception:
            return {
                "ok": False,
                "mensaje": "Ocurrió un error inesperado al buscar ISBN"
            }