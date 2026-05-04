from Infraestructura.BibliotecaEjemplares import BibliotecaEjemplares
b = BibliotecaEjemplares()
r = b.get("ADQ-0000209")
print(r.getBody())
print(r.getLibro().getBody())