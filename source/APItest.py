from Infraestructura.API.BibliotecaEjemplares import BibliotecaEjemplares
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos
import uuid
b = BibliotecaPrestamos()
res = b.getDetalle("f8397485-9703-4490-8662-0afba2f5c143")
print(res)

