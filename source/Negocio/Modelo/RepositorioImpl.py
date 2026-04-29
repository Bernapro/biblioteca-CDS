from Negocio.Modelo.Interfaces.Repositorio import Repositorio
from Persistencia.CRUD.CRUDimpl import CRUDimp

class RepositorioImpl(Repositorio):

    def __init__(self, crud: CRUDimp):
        self.__crud = crud


#registro
    def obtener_todos(self, nombre_tabla: str):
        return self.__crud.read_all(nombre_tabla)

    def obtener_por_id(self, nombre_tabla: str, id):
        return self.__crud.read_one(
            nombre_tabla,
            {f"id_{nombre_tabla}": id}
        )

    def guardar(self, objeto):
        if self.__crud:
            valores = tuple(objeto.get_columns().values())
            return self.__crud.create(objeto.get_table_name(), objeto.get_columns().keys(), valores)
        return None
        
    def eliminar(self, nombre_tabla: str, id):
        return self.__crud.delete(
            nombre_tabla,
            {f"id_{nombre_tabla}": id}
        )
    
    #asistencia
    def buscar_usuario_por_identificador(self, identificador):
        return self.__crud.read_one(
            "usuario",
            {"identificador": identificador}
        )

    def obtener_registro_abierto(self, id_usuario):
        return self.__crud.read_one(
            "registro",
            {
                "id_usuario": id_usuario,
                "hora_salida": None
            }
        )

    def registrar_salida(self, id_registro, hora_salida):
        return self.__crud.update(
            "registro",
            {"hora_salida": hora_salida},
            {"id_registro": id_registro}
        )