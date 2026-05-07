from Infraestructura.API.libros_api import (
    obtener_libros,
    obtener_libro_por_isbn
)


class ControladorLibros:

    def listar_libros(self, pagina, tamanio, busqueda):
        response = obtener_libros(
            n_page=pagina,
            length=tamanio,
            busqueda=busqueda
        )

        if response.status_code != 200:
            return None

        datos = response.json()

        libros_raw = datos.get("contenido", [])

        libros = [
            {
                "titulo": l.get("titulo", "Sin título"),
                "isbn": l.get("isbn", "N/A"),
                "ejemplares": l.get("Ejemplares", 0)
            }
            for l in libros_raw
        ]

        total_paginas = datos.get("totalPaginas", 1)
        total_elementos = datos.get("totalElementos", 0)

        # cálculo de rango 
        if total_elementos == 0:
            inicio = 0
            fin = 0
        else:
            inicio = (pagina * tamanio) + 1
            fin = min(inicio + len(libros) - 1, total_elementos)

        return {
            "libros": libros,
            "total_paginas": total_paginas,
            "total_elementos": total_elementos,
            "inicio": inicio,
            "fin": fin
        }

    def obtener_detalle(self, isbn):
        response = obtener_libro_por_isbn(isbn)

        if response.status_code != 200:
            return None

        libro = response.json()

        return {
            "titulo": libro.get("titulo", "Sin título"),
            "isbn": libro.get("isbn", "N/A"),
            "editorial": libro.get("editorial", "N/A"),
            "ejemplares": libro.get("nEjemplares", 0),
            "edicion": libro.get("edicion", "N/A"),
            "fecha": libro.get("fechaPublicacion", "N/A"),
            "dewey": libro.get("dewey", "N/A"),
            "lcc": libro.get("clasificacionDelCongreso") or "Sin clasificación",
            "cdu": libro.get("decimalUniversal") or "Sin clasificación",
            "autores": ", ".join(libro.get("autores", [])) or "Sin autores",
            "categorias": ", ".join(libro.get("categorias", [])) or "Sin categorías",
        }