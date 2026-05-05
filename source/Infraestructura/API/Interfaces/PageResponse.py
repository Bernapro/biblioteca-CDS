from Infraestructura.API.Interfaces.ResponseObject import ResponseObject
from dataclasses import dataclass, field
from typing import Generic
from Infraestructura.API.Interfaces.PageMetadata import PageMetadata
from Infraestructura.API.Interfaces.PageMetadata import T


@dataclass
class PageResponse(Generic[T]):
    content: list[T] = field(default_factory=list)
    metadata: PageMetadata = field(default_factory=PageMetadata)