from Infraestructura.API.BibliotecaEjemplares import BibliotecaEjemplares
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos

b = BibliotecaPrestamos()
r = b.getEstado()
print(r.getBody() if r else "None")