from dataclasses import dataclass, field
from typing import TypeVar

# Definimos una variable de tipo genérico (equivalente a la <T> en Java)
T = TypeVar('T')

@dataclass
class PageMetadata:
    total_pages: int = 0
    total_elements: int = 0
    size: int = 0
    number: int = 0
    last: bool = True
