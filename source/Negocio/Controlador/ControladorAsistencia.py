
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db
from Negocio.Modelo.Registro import Registro


class ControladorAsistencia:

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp(db))

    def procesar_qr(self, e):

        if e.control.data == "btn_qr":

            qr = self.__pantalla.input_qr.value.strip()

            if not qr:
                return {"estado": "INVALIDO", "nombre": ""}

            usuario = self.__repo.buscar_usuario_por_identificador(qr)

            if not usuario:
                return {"estado": "NO_ENCONTRADO", "nombre": ""}

            id_usuario = usuario["id_usuario"]

            nombre_completo = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"
# cerrar registros viejos primero
            self.__repo.cerrar_registros_abiertos()
            registro_abierto = self.__repo.obtener_registro_abierto(id_usuario)

            if not registro_abierto:
                nuevo = Registro(id_usuario=id_usuario)
                self.__repo.guardar(nuevo)
                estado = "ENTRADA"

            else:
                self.__repo.registrar_salida(
                    registro_abierto["id_registro"]
                )
                estado = "SALIDA"

            self.__pantalla.input_qr.value = ""
            self.__pantalla.update()

            return {
                "estado": estado,
                "nombre": nombre_completo
            }