import requests

BASE_URL = "http://localhost:8080/biblioteca/libros"


def obtener_libros(n_page=0, length=100, busqueda=""):
    params = {
        "nPage": n_page,
        "len": length
    }

    if busqueda:
        params["busqueda"] = busqueda

    return requests.get(
        BASE_URL,
        params=params
    )

def obtener_libro_por_isbn(isbn):
    return requests.get(f"{BASE_URL}/{isbn}")

def crear_libro(data):
    return requests.post(BASE_URL, json=data)