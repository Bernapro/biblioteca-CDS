import requests

BASE_URL = "http://localhost:8080/biblioteca/libros"

# LISTAR LIBROS (PAGINADO)
def obtener_libros(n_page=0, length=100, busqueda=""):
    params = {
        "nPage": n_page,
        "len": length
    }

    if busqueda:
        params["busqueda"] = busqueda

    try:
        return requests.get(BASE_URL, params=params)
    except Exception as e:
        print("Error obtener_libros:", e)
        return None

# DETALLE POR ISBN
def obtener_libro_por_isbn(isbn):
    try:
        return requests.get(f"{BASE_URL}/{isbn}")
    except Exception as e:
        print("Error obtener_libro_por_isbn:", e)
        return None

# CREAR LIBRO
def crear_libro(data):
    try:
        return requests.post(BASE_URL, json=data)
    except Exception as e:
        print("Error crear_libro:", e)
        return None

# BUSCAR DATOS AUTOMÁTICOS POR ISBN
def autocompletar_libro(isbn):
    try:
        return requests.get(f"{BASE_URL}/autocompletar/{isbn}")
    except Exception as e:
        print("Error autocompletar_libro:", e)
        return None