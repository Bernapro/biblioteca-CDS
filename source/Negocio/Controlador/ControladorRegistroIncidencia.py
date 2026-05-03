from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Negocio.Modelo.Incidencia import Incidencia


class ControladorRegistroIncidencia:

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp())

    # =========================
    # 🔍 BUSCAR USUARIO AUTOMÁTICO
    # =========================
    def buscar_usuario(self, e):
        identificador = self.__pantalla.text_identificador.value.strip()

        if not identificador:
            self.__pantalla.txt_nombre.value = ""
            self.__pantalla.id_usuario = None
            self.__pantalla.update()
            return

        usuario = self.__repo.buscar_usuario_por_identificador(identificador)

        if usuario:
            nombre = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"

            self.__pantalla.txt_nombre.value = nombre
            self.__pantalla.txt_nombre.disabled = True

            self.__pantalla.tipo_usuario = usuario["tipo_usuario"]
            self.__pantalla.id_usuario = usuario["id_usuario"]

            self.__pantalla.txt_mensaje.value = ""
        else:
            self.__pantalla.txt_nombre.value = "Usuario no encontrado"
            self.__pantalla.txt_nombre.disabled = True
            self.__pantalla.id_usuario = None

            self.__pantalla.txt_mensaje.value = "❌ Identificador no válido"
            self.__pantalla.txt_mensaje.color = "red"

        self.__pantalla.update()

    # =========================
    # 💾 GUARDAR INCIDENCIA
    # =========================
    def guardar(self, e):

        # =========================
        # 🔥 VALIDACIONES COMPLETAS
        # =========================

        if not hasattr(self.__pantalla, "id_usuario") or not self.__pantalla.id_usuario:
            self.__pantalla.txt_mensaje.value = "❌ Debes seleccionar un usuario válido"
            self.__pantalla.txt_mensaje.color = "orange"
            self.__pantalla.update()
            return

        if not self.__pantalla.drop_tipo.value:
            self.__pantalla.txt_mensaje.value = "❌ Selecciona el tipo de incidencia"
            self.__pantalla.txt_mensaje.color = "orange"
            self.__pantalla.update()
            return

        if not self.__pantalla.drop_cat.value:
            self.__pantalla.txt_mensaje.value = "❌ Selecciona la categoría"
            self.__pantalla.txt_mensaje.color = "orange"
            self.__pantalla.update()
            return

        if not self.__pantalla.txt_desc.value or not self.__pantalla.txt_desc.value.strip():
            self.__pantalla.txt_mensaje.value = "❌ Ingresa una descripción"
            self.__pantalla.txt_mensaje.color = "orange"
            self.__pantalla.update()
            return

        if not self.__pantalla.txt_lugar.value or not self.__pantalla.txt_lugar.value.strip():
            self.__pantalla.txt_mensaje.value = "❌ Ingresa el lugar"
            self.__pantalla.txt_mensaje.color = "orange"
            self.__pantalla.update()
            return

        try:
            # =========================
            # 🔥 NORMALIZAR ENUMS
            # =========================
            tipo = self.__pantalla.drop_tipo.value.upper().strip()

            data = {
                "id_usuario": self.__pantalla.id_usuario,
                "tipo": tipo,
                "motivo": self.__pantalla.drop_cat.value,
                "descripcion": self.__pantalla.txt_desc.value.strip(),
                "lugar": self.__pantalla.txt_lugar.value.strip()
            }

            incidencia = Incidencia()
            incidencia.set_data(data)

            resultado = self.__repo.guardar(incidencia)

            if resultado:
                nombre = self.__pantalla.txt_nombre.value
                identificador = self.__pantalla.text_identificador.value

                self.__pantalla.txt_mensaje.value = f"✅ Incidencia registrada para {nombre} ({identificador})"
                self.__pantalla.txt_mensaje.color = "green"

                self.limpiar_form()
            else:
                self.__pantalla.txt_mensaje.value = "❌ No se pudo guardar la incidencia"
                self.__pantalla.txt_mensaje.color = "red"

        except Exception as ex:
            self.__pantalla.txt_mensaje.value = "💥 Error al guardar la incidencia"
            self.__pantalla.txt_mensaje.color = "red"
            print("💥 ERROR REAL:", ex)

        self.__pantalla.update()

    # =========================
    # 🧹 LIMPIAR FORMULARIO
    # =========================
    def limpiar_form(self):
        self.__pantalla.txt_nombre.value = ""
        self.__pantalla.txt_nombre.disabled = False

        self.__pantalla.text_identificador.value = ""
        self.__pantalla.txt_desc.value = ""
        self.__pantalla.txt_lugar.value = ""

        self.__pantalla.drop_tipo.value = "PARCIAL"
        self.__pantalla.drop_cat.value = "Libros"

        self.__pantalla.id_usuario = None

        self.__pantalla.update()