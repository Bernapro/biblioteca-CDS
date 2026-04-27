from abc import ABC, abstractmethod
from psycopg import sql
from psycopg import Connection
from psycopg.rows import dict_row
from Persistencia.Postgres.PostgresOperable import PostgresOperable

class CRUD(ABC):
    INSERT = "INSERT INTO {tabla} ({columnas}) VALUES ({valores}) RETURNING *"
    
    @abstractmethod
    def create(self, nombre_tabla: str, columnas: dict, valores: tuple) -> dict:
        pass