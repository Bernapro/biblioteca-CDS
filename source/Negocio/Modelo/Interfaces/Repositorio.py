from abc import ABC, abstractmethod
from Persistencia.Postgres.PostgresOperable import PostgresOperable


class Repositorio(ABC):

    @abstractmethod
    def obtener_todos(self, nombre_tabla: str):
        pass

    @abstractmethod
    def obtener_por_id(self, nombre_tabla: str, id):
        pass

    @abstractmethod
    def guardar(self, objeto: PostgresOperable):
        pass

    @abstractmethod
    def eliminar(self, nombre_tabla: str, id):
        pass