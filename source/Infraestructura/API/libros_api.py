import requests

BASE_URL = "http://localhost:8080/biblioteca/libros"


def obtener_libros(n_page=0, length=100):
    return requests.get(
        BASE_URL,
        params={
            "nPage": n_page,
            "len": length
        }
    )


def crear_libro(data):
    return requests.post(BASE_URL, json=data)