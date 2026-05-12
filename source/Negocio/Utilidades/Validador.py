import flet as ft
from datetime import datetime

class Validador:
    COLOR_ERROR = "#EF4444"
    COLOR_NORMAL = "#D1D5DB"
    @staticmethod
    def validar(campos: list):
        Validador._limpiar_estilos(campos)
        for control, mensaje in campos:
            if hasattr(control, "visible") and not control.visible:
                continue
            valor = control.value
            if isinstance(control, ft.Dropdown):
                if valor is None or valor in ["", "Todos", "Selecciona"]:
                    Validador._marcar_error(control)
                    texto = mensaje or f"Selecciona '{control.label}'"
                    return False, texto
            else:
                if valor is None or str(valor).strip() == "":
                    Validador._marcar_error(control)
                    texto = mensaje or f"Completa el campo '{control.label}'"
                    return False, texto
        return True, None

    @staticmethod
    def _limpiar_estilos(campos):
        for control, _ in campos:
            if hasattr(control, "border_color"):
                control.border_color = Validador.COLOR_NORMAL
                if hasattr(control, "update"):
                    control.update()

    @staticmethod
    def _marcar_error(control):
        if hasattr(control, "border_color"):
            control.border_color = Validador.COLOR_ERROR
        if hasattr(control, "update"):
            control.update()

    @staticmethod
    def limpiar(controles: list):
        for c in controles:
            if isinstance(c, ft.TextField):
                c.value = ""
            elif isinstance(c, ft.Dropdown):
                c.value = None
            elif hasattr(c, "controls"):
                Validador.limpiar(c.controls)

    @staticmethod
    def limpiar__mod(controles: list):
        for c in controles:
            if isinstance(c, ft.TextField):
                c.value = ""
                
            elif isinstance(c, ft.Dropdown):
                c.value = None
                
            elif hasattr(c, "controls"):
                Validador.limpiar(c.controls)
                
            elif hasattr(c, "content") and c.content is not None:
                Validador.limpiar([c.content])

    @staticmethod
    def validar_rango_fechas(fecha_inicio, fecha_fin):

        if not fecha_inicio or not fecha_fin:
            return True, None

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

            if inicio > fin:
                return False, "La fecha inicio no puede ser mayor a la fecha fin"

            return True, None

        except Exception:
            return False, "Formato de fecha inválido"