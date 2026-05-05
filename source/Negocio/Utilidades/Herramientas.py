import flet as ft

class Herramientas:

    @staticmethod
    def reset_dropdown(dropdown: ft.Dropdown):
        if dropdown is None:
            return

        #EL SECRETO: Flet a veces ignora 'None', pero obedece inmediatamente al string vacío ""
        dropdown.value = "" 
        dropdown.update()

    @staticmethod
    def reset_dropdowns(dropdowns: list):
        for d in dropdowns:
            Herramientas.reset_dropdown(d)

    @staticmethod
    def limpiar_control(control):
        if isinstance(control, ft.TextField):
            control.value = ""
            control.update()
        elif isinstance(control, ft.Dropdown):
            Herramientas.reset_dropdown(control)
        elif hasattr(control, "controls"): 
            Herramientas.limpiar_controles(control.controls)

    @staticmethod
    def limpiar_controles(controles: list):
        for c in controles:
            Herramientas.limpiar_control(c)

    @staticmethod
    def mostrar(controles: list):
        for c in controles:
            c.visible = True
            c.update()

    @staticmethod
    def ocultar(controles: list):
        for c in controles:
            c.visible = False
            c.update()

    @staticmethod
    def habilitar(controles: list):
        for c in controles:
            if hasattr(c, "disabled"):
                c.disabled = False
                c.update()

    @staticmethod
    def deshabilitar(controles: list):
        for c in controles:
            if hasattr(c, "disabled"):
                c.disabled = True
                c.update()

    