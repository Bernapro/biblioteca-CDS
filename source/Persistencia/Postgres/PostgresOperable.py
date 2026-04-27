from abc import ABC, abstractmethod 

class PostgresOperable(ABC):
    
    @abstractmethod
    def get_table_name(self) -> str:
        pass

    @abstractmethod
    def get_columns(self) -> dict:
        pass

    @abstractmethod
    def get_pkey(self) -> dict:
        pass

    @abstractmethod
    def set_columns(self, args: dict):
        pass

    @abstractmethod
    def set_pkeys(self, args: dict):
        pass

