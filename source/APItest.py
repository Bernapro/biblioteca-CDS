from Infraestructura.API.BibliotecaEjemplares import BibliotecaEjemplares
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos
import uuid
b = BibliotecaEjemplares()
res = b.getEstado()
print(res.getBody())

