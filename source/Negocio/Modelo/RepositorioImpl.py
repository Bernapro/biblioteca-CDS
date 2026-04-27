from Negocio.Modelo.Interfaces.Repositorio import Repositorio
from Persistencia.CRUD.CRUDimpl import CRUDimp

class RepositorioImpl(Repositorio):

    def __init__(self, crud: CRUDimp):
        self.__crud = crud



    def obtener_todos(self):
        pass

    def obtener_por_id(self, id):
        pass

    def guardar(self, objeto):
        if self.__crud:
            valores = tuple(objeto.get_columns().values())
            self.__crud.create(objeto.get_table_name(), objeto.get_columns().keys(), valores)
        

    def eliminar(self, id):
        pass