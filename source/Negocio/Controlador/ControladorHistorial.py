from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class ControladorHistorial:

    def __init__(self):
        self.__repo = RepositorioImpl(CRUDimp(db))

    def obtener_historial(self, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        self.__repo.cerrar_registros_abiertos()

        datos = self.__repo.obtener_historial(
            texto,
            fecha_inicio,
            fecha_fin,
            tipo,
            estado
        )

        resultado = []

        for d in datos:
            nombre = f"{d['nombre']} {d['ap_paterno']} {d['ap_materno']}"

            resultado.append({
                "identificador": d["identificador"],
                "nombre": nombre,
                "tipo": d["tipo_usuario"],
                "fecha": d["fecha_entrada"].strftime("%Y-%m-%d"),
                "entrada": d["fecha_entrada"].strftime("%H:%M:%S"),
                "salida": d["fecha_salida"].strftime("%H:%M:%S") if d["fecha_salida"] else "-"
            })

        return resultado
    
    def contar_hoy(self):
        return self.__repo.contar_usuarios_hoy()
    

    def obtener_historial_completo(self, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        self.__repo.cerrar_registros_abiertos()

        datos = self.__repo.obtener_historial_completo(
            texto,
            fecha_inicio,
            fecha_fin,
            tipo,
            estado
        )

        resultado = []

        for d in datos:
            resultado.append({
                "id": d["id_registro"],
                "identificador": d["identificador"],
                "nombre": f"{d['nombre']} {d['ap_paterno']} {d['ap_materno']}",
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
            })

        return resultado
    
    def exportar_excel(self, ruta, texto="", fecha_inicio=None, fecha_fin=None, tipo="Todos", estado="Todos"):
        import openpyxl
        from openpyxl.utils import get_column_letter
        datos = self.obtener_historial_completo(
            texto, fecha_inicio, fecha_fin, tipo, estado
        )

        import openpyxl
        from openpyxl.utils import get_column_letter

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
                d.get("id"),
                d.get("identificador"),
                d.get("nombre"),
                d.get("tipo"),
                d.get("entrada"),
                d.get("salida"),
                d.get("matricula"),
                d.get("n_plaza"),
                d.get("grupo"),
                d.get("carrera"),
                d.get("facultad"),
                d.get("semestre"),
                d.get("institucion"),
            ])

        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length + 2

        wb.save(ruta)