from abc import ABC, abstractmethod


class Repositorio(ABC):
    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def obtener_por_id(self, id):
        pass

    @abstractmethod
    def guardar(self, entidad):
        pass

    @abstractmethod
    def eliminar(self, id):
        pass