from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class ControladorHistorial:

    def __init__(self):
        self.__repo = RepositorioImpl(CRUDimp(db))

    def obtener_historial(self, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        self.__repo.cerrar_registros_abiertos()

        datos = self.__repo.obtener_historial(
            texto,
            fecha_inicio,
            fecha_fin,
            tipo,
            estado
        )

        resultado = []

        for d in datos:
            nombre = f"{d['nombre']} {d['ap_paterno']} {d['ap_materno']}"

            resultado.append({
                "identificador": d["identificador"],
                "nombre": nombre,
                "fecha": d["fecha_entrada"].strftime("%Y-%m-%d"),
                "entrada": d["fecha_entrada"].strftime("%H:%M:%S"),
                "salida": d["fecha_salida"].strftime("%H:%M:%S") if d["fecha_salida"] else "-"
            })

        return resultado
    
    def contar_hoy(self):
        return self.__repo.contar_usuarios_hoy()