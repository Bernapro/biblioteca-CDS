from Infraestructura.API.BibliotecaEjemplares import BibliotecaEjemplares
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos
import uuid
b = BibliotecaPrestamos()
res = b.getDetalle("284a9fda-e5c9-4626-a752-0e6b9a076ae2")
print(res)
