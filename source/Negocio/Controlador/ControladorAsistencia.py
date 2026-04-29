from datetime import datetime

from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db
from Negocio.Modelo.Registro import Registro


class ControladorAsistencia:

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp(db))

    def procesar_qr(self, e):
        id_control = e.control.data

        if id_control == "btn_qr":

            qr = self.__pantalla.input_qr.value.strip()


            if not qr or len(qr) < 3:
                return {"estado": "INVALIDO", "nombre": ""}


            usuario = self.__repo.buscar_usuario_por_identificador(qr)

            if not usuario:
                return {"estado": "NO_ENCONTRADO", "nombre": ""}

            id_usuario = usuario["id_usuario"]

            nombre_completo = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"


            registros = self.__repo.obtener_todos("registro")

            registro_abierto = None

            for r in reversed(registros):
                if r["id_usuario"] == id_usuario and r["hora_salida"] is None:
                    registro_abierto = r
                    break

            # =========================
            # DECISIÓN
            # =========================
            if not registro_abierto:
                nuevo = Registro(id_usuario=id_usuario)
                self.__repo.guardar(nuevo)

                estado = "ENTRADA"

            else:
                hora_salida = datetime.now().time()

                self.__repo.registrar_salida(
                    registro_abierto["id_registro"],
                    hora_salida
                )

                estado = "SALIDA"


            self.__pantalla.input_qr.value = ""
            self.__pantalla.update()

            return {
                "estado": estado,
                "nombre": nombre_completo
            }