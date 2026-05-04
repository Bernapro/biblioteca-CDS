from Infraestructura.API.libros_api import crear_libro


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