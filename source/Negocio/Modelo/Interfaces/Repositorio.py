from abc import ABC, abstractmethod
from Persistencia.Postgres.PostgresOperable import PostgresOperable


class Repositorio(ABC):
    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def obtener_por_id(self, id):
        pass

    @abstractmethod
    def guardar(self, objeto: PostgresOperable):
        pass

    @abstractmethod
    def eliminar(self, id):
        pass