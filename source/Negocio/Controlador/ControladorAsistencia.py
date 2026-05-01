
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db
from Negocio.Modelo.Registro import Registro


class ControladorAsistencia:

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp())

    def procesar_qr(self, e):
        estado = "NO_ENCONTRADO"
        nombre_completo = ""
        usuario = None
        if e.control.data == "btn_qr":

            usuario = None
            qr = self.__pantalla.input_qr.value.strip()

            if not qr:
                return {"estado": "INVALIDO", "nombre": ""}

            with db.get_connection() as conn:
                usuario = self.__repo.buscar_usuario_por_identificador(qr, conn)
                print(usuario)
                if not usuario:
                    return {"estado": estado, "nombre": nombre_completo}

                id_usuario = usuario["id_usuario"]

                nombre_completo = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"

            # cerrar registros viejos primero
                self.__repo.cerrar_registros_abiertos(conn)
                registro_abierto = self.__repo.obtener_registro_abierto(id_usuario, conn)

                if not registro_abierto:
                    nuevo = Registro(id_usuario=id_usuario)
                    self.__repo.guardar(nuevo, conn)
                    estado = "ENTRADA"

                else:
                    self.__repo.registrar_salida(registro_abierto["id_registro"], conn)
                    estado = "SALIDA"

            self.__pantalla.input_qr.value = ""
            self.__pantalla.update()

            return {
                "estado": estado,
                "nombre": nombre_completo,
                "tipo": usuario.get("tipo_usuario") if usuario else None  
            }