
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

            usuario = self.__repo.buscar_usuario_por_identificador(qr)
            print(usuario)
            if not usuario:
                return {"estado": estado, "nombre": nombre_completo}

            id_usuario = usuario["id_usuario"]

            nombre_completo = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"

            # Cerrar registros viejos primero (procedimiento)
            self.__repo.ejecutar_procedimiento("cerrar_registros_pendientes")
            
            # Procesar asistencia
            registro_abierto = self.__repo.obtener_registro_abierto(id_usuario)

            if not registro_abierto:
                nuevo = Registro(id_usuario=id_usuario)
                self.__repo.guardar(nuevo)
                estado = "ENTRADA"

            else:
                self.__repo.registrar_salida(registro_abierto["id_registro"])
                estado = "SALIDA"

            self.__pantalla.input_qr.value = ""
            self.__pantalla.update()

            return {
                "estado": estado,
                "nombre": nombre_completo,
                "tipo": usuario.get("tipo_usuario") if usuario else None  
            }