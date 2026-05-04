from Infraestructura.BibliotecaEjemplares import BibliotecaEjemplares
b = BibliotecaEjemplares()
r = b.get("ADQ-0083961")
print(r.getBody())
print(r.getLibro().getBody())