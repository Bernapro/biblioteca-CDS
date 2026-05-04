from abc import ABC, abstractmethod

class ResponseObject(ABC):

    @abstractmethod
    def setBody(self, args: dict)-> None:
        pass
    
    @abstractmethod
    def getBody(self) -> dict:
        pass