from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class ControladorHistorial:

    def __init__(self):
        self.__repo = RepositorioImpl(CRUDimp(db))

    def obtener_historial(self):
        self.__repo.cerrar_registros_abiertos()

        datos = self.__repo.obtener_historial()

        resultado = []

        for d in datos:
            nombre = f"{d['nombre']} {d['ap_paterno']} {d['ap_materno']}"

            fecha_entrada = d["fecha_entrada"]
            fecha_salida = d["fecha_salida"]

            resultado.append({
                "identificador": d["identificador"],
                "nombre": nombre,
                "fecha": fecha_entrada.strftime("%Y-%m-%d"),
                "entrada": fecha_entrada.strftime("%H:%M:%S"),
                "salida": fecha_salida.strftime("%H:%M:%S") if fecha_salida else "-"
            })

        return resultado