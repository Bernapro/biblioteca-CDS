from Infraestructura.API.BibliotecaEjemplares import BibliotecaEjemplares
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos

b = BibliotecaPrestamos()
r = b.getPage(nPage = None, len = None)

print(r)