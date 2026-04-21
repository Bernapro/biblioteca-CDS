import json
from datetime import datetime

RUTA = "datos/datos.json"


def cargar_datos():
    with open(RUTA, "r") as f:
        return json.load(f)


def guardar_datos(data):
    with open(RUTA, "w") as f:
        json.dump(data, f, indent=4)


def registrar_qr(qr):
    data = cargar_datos()

    usuario = next(
        (u for u in data["usuarios"] if u["identificador"] == qr),
        None
    )

    if not usuario:
        return "❌ Usuario no encontrado"

    nombre_completo = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")

    registros_usuario = [
        r for r in data["registros"]
        if r["id_usuario"] == usuario["id_usuario"]
    ]

    # Entrada o salida
    if registros_usuario and registros_usuario[-1]["hora_salida"] is None:
        registros_usuario[-1]["hora_salida"] = hora
        mensaje = f"👋 Salida registrada: {nombre_completo}"
    else:
        data["registros"].append({
            "id_usuario": usuario["id_usuario"],
            "identificador": usuario["identificador"],
            "nombre": nombre_completo,
            "fecha": fecha,
            "hora_entrada": hora,
            "hora_salida": None
        })
        mensaje = f"✅ Entrada registrada: {nombre_completo}"

    guardar_datos(data)

    return mensaje