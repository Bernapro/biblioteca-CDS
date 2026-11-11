import os
from decimal import Decimal
from Persistencia.Postgres.ReporteRepositoryImpl import ReporteRepositoryImpl
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp


class ControladorReportes:

    def __init__(self, repo=None):
        self.repo = repo or ReporteRepositoryImpl()
        self._repo_general = RepositorioImpl(CRUDimp())

    def generar_reporte(self, tipo, fecha_inicio=None, fecha_fin=None, tipo_usuario=None):
        self._repo_general.cerrar_registros_pendientes()

        if tipo_usuario:
            tipo_usuario = str(tipo_usuario).upper()
            if tipo_usuario in ("TODOS", "TODO"):
                tipo_usuario = None
            elif tipo_usuario == "ALUMNOS":
                tipo_usuario = "ALUMNO"
            elif tipo_usuario == "VISITANTES":
                tipo_usuario = "VISITANTE"

        try:
            if tipo == "Asistencia completa":
                res = self.repo.obtener_asistencia_completa(
                    fecha_inicio,
                    fecha_fin,
                    tipo_usuario
                )

            elif tipo == "Usuarios más activos":
                res = self.repo.obtener_usuarios_mas_activos(
                    fecha_inicio,
                    fecha_fin,
                    tipo_usuario
                )

            elif tipo in ("Horas pico avanzado", "Horas pico"):
                res = self.repo.obtener_horas_pico_avanzado(
                    fecha_inicio,
                    fecha_fin
                )

            elif tipo == "Tendencia diaria":
                res = self.repo.obtener_tendencia_diaria(
                    fecha_inicio,
                    fecha_fin,
                    tipo_usuario
                )

            elif tipo == "Reporte por carrera":
                res = self.repo.obtener_reporte_carreras(
                    fecha_inicio,
                    fecha_fin
                )

            elif tipo == "Reporte por facultad":
                res = self.repo.obtener_reporte_facultades(
                    fecha_inicio,
                    fecha_fin
                )

            elif tipo == "Reporte por semestre":
                res = self.repo.obtener_reporte_semestres(
                    fecha_inicio,
                    fecha_fin
                )

            elif tipo == "Visitantes externos":
                res = self.repo.obtener_visitantes_externos(
                    fecha_inicio,
                    fecha_fin
                )

            elif tipo == "Reporte de saturación":
                res = self.repo.obtener_reporte_saturacion(
                    fecha_inicio,
                    fecha_fin
                )

            elif tipo == "Reporte de crecimiento":
                res = self.repo.obtener_reporte_crecimiento()

            else:
                return []

            return res if res is not None else []

        except Exception as e:
            print(f"Error al generar reporte '{tipo}': {e}")
            return []

    def exportar_excel(
        self,
        ruta,
        tipo=None,
        fecha_inicio=None,
        fecha_fin=None,
        tipo_usuario=None,
        columnas=None,
        filas=None
    ):
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment
            from openpyxl.utils import get_column_letter

            if not ruta:
                return False

            usar_tabla = bool(columnas and filas and len(filas) > 0)

            if not usar_tabla:
                # obtener datos del reporte desde el repositorio
                datos = self.generar_reporte(
                    tipo=tipo,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    tipo_usuario=tipo_usuario
                )

                # validar datos vacíos
                if not datos:
                    return False

                # validar formato
                if not isinstance(datos[0], dict):
                    raise ValueError("El reporte no tiene formato diccionario")

                headers = list(datos[0].keys())
                filas_excel = [list(d.values()) for d in datos]
            else:
                headers = [str(col) for col in columnas]
                filas_excel = filas

            directorio = os.path.dirname(ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

            # crear workbook
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Reporte"

            # HEADERS
            ws.append(headers)
            header_font = Font(bold=True)
            for cell in ws[1]:
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # DATOS
            for fila_orig in filas_excel:
                fila = []
                for valor in fila_orig:
                    # convertir fechas y tipos especiales automáticamente
                    if hasattr(valor, "strftime"):
                        valor = valor.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(valor, Decimal):
                        valor = float(valor)
                    elif not isinstance(valor, (int, float, str, bool)) and valor is not None:
                        valor = str(valor)

                    fila.append(valor)

                ws.append(fila)

            # AUTO AJUSTE COLUMNAS
            for col in ws.columns:
                max_length = 0
                col_letter = get_column_letter(col[0].column)

                for cell in col:
                    if cell.value is not None:
                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                ws.column_dimensions[col_letter].width = max_length + 3

            # GUARDAR
            wb.save(ruta)
            return True

        except Exception as e:
            print(f"Error al exportar Excel: {e}")
            return False
