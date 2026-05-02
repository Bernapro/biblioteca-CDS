from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class ControladorHistorial:

    def __init__(self):
        self.__repo = RepositorioImpl(CRUDimp())

    # =========================
    # BASE (REUTILIZABLE)
    # =========================
    def obtener_datos(self):
        """Obtiene datos del historial:
        1. Cierra registros abiertos del día anterior
        2. Retorna vista_historial completa
        """
        # Ejecutar procedimiento para cerrar registros pendientes
        self.__repo.ejecutar_procedimiento("cerrar_registros_pendientes")
        
        # Obtener datos desde la vista
        return self.__repo.obtener_todos("vista_historial")

    def filtrar(self, datos, texto, fecha_inicio, fecha_fin, tipo, estado):
        """Filtra datos en memoria (lógica de negocio Python)"""
        resultado = []

        for d in datos:

            # TEXTO
            if texto:
                t = texto.lower()
                if t not in d["nombre_completo"].lower() and t not in d["identificador"].lower():
                    continue

            # FECHAS
            if fecha_inicio and d["fecha_entrada"].date() < fecha_inicio:
                continue

            if fecha_fin and d["fecha_entrada"].date() > fecha_fin:
                continue

            # TIPO
            if tipo != "Todos" and d["tipo_usuario"] != tipo.upper():
                continue

            # ESTADO
            if estado == "Activos" and d["fecha_salida"] is not None:
                continue

            if estado == "Finalizados" and d["fecha_salida"] is None:
                continue

            resultado.append(d)

        return resultado

    # =========================
    # MAPEADORES
    # =========================
    def mapear_simple(self, datos):
        """Mapea datos completos a formato simple para tabla"""
        return [
            {
                "identificador": d["identificador"],
                "nombre": d["nombre_completo"],
                "tipo": d["tipo_usuario"],
                "fecha": d["fecha_entrada"].strftime("%Y-%m-%d"),
                "entrada": d["fecha_entrada"].strftime("%H:%M:%S"),
                "salida": d["fecha_salida"].strftime("%H:%M:%S") if d["fecha_salida"] else "-"
            }
            for d in datos
        ]

    def mapear_completo(self, datos):
        """Mapea datos para modal de detalles (sin transformación de fechas)"""
        return [
            {
                "id": d["id_registro"],
                "identificador": d["identificador"],
                "nombre": d["nombre_completo"],
                "tipo": d["tipo_usuario"],
                "entrada": d["fecha_entrada"],
                "salida": d["fecha_salida"],
                "matricula": d["matricula"],
                "n_plaza": d["n_plaza"],
                "grupo": d["grupo"],
                "carrera": d["nombre_carrera"],
                "facultad": d["nombre_facultad"],
                "semestre": d["semestre"],
                "institucion": d["nombre_institucion"]
            }
            for d in datos
        ]

    # =========================
    # PUBLICOS
    # =========================
    def obtener_historial(self, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        """Retorna historial filtrado y formateado para tabla"""
        if fecha_inicio and isinstance(fecha_inicio, str):
            from datetime import datetime
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        if fecha_fin and isinstance(fecha_fin, str):
            from datetime import datetime
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        datos = self.obtener_datos()
        filtrados = self.filtrar(datos, texto, fecha_inicio, fecha_fin, tipo, estado)
        return self.mapear_simple(filtrados)

    def obtener_historial_completo(self, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        """Retorna historial completo para detalles y Excel"""
        if fecha_inicio and isinstance(fecha_inicio, str):
            from datetime import datetime
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        if fecha_fin and isinstance(fecha_fin, str):
            from datetime import datetime
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        datos = self.obtener_datos()
        filtrados = self.filtrar(datos, texto, fecha_inicio, fecha_fin, tipo, estado)
        return self.mapear_completo(filtrados)

    def contar_usuarios_hoy(self):
        """Retorna total de usuarios únicos que asistieron hoy
        Procesa datos de vista_historial en memoria (reutilización)
        """
        datos = self.obtener_datos()
        usuarios_hoy = set()
        
        for d in datos:
            if d["fecha_entrada"].date() == self._get_today():
                usuarios_hoy.add(d["id_usuario"])
        
        return len(usuarios_hoy)

    def _get_today(self):
        """Helper para obtener fecha de hoy"""
        from datetime import date
        return date.today()

    # =========================
    # EXPORTAR EXCEL
    # =========================
    def exportar_excel(self, ruta, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        """Exporta historial filtrado a Excel"""
        if fecha_inicio and isinstance(fecha_inicio, str):
            from datetime import datetime
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        if fecha_fin and isinstance(fecha_fin, str):
            from datetime import datetime
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        import openpyxl
        from openpyxl.utils import get_column_letter

        datos = self.obtener_historial_completo(
            texto, fecha_inicio, fecha_fin, tipo, estado
        )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Historial"

        headers = [
            "ID", "Identificador", "Nombre", "Tipo",
            "Entrada", "Salida",
            "Matrícula", "Plaza",
            "Grupo", "Carrera", "Facultad", "Semestre", "Institución"
        ]

        ws.append(headers)

        for d in datos:
            ws.append([
                d["id"],
                d["identificador"],
                d["nombre"],
                d["tipo"],
                d["entrada"],
                d["salida"],
                d["matricula"],
                d["n_plaza"],
                d["grupo"],
                d["carrera"],
                d["facultad"],
                d["semestre"],
                d["institucion"],
            ])

        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length + 2

        wb.save(ruta)